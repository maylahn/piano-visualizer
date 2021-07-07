import os
import mido
import time

from settings import *
from strip import Strip
from audio import Audio
from modes import dualcolor, fft, monochrome, multicolor, rainbow, c_major
from key import Key


class Piano:
    def __init__(self, mic_active=True):
        self.access_settings_timer = None
        self.midi_connection = None
        self.keyboard = Key.init_keyboard()
        self.modes = [
            c_major.cMajor(self.keyboard),
            dualcolor.Dualcolor(self.keyboard),
            monochrome.Monochrome(self.keyboard),
            multicolor.Multicolor(self.keyboard),
            rainbow.Rainbow(self.keyboard),
        ]
        if mic_active:
            self.modes += [fft.FFT(self.keyboard, Audio())]
        self.active_mode = (
            next((mode for mode in self.modes if mode.name == PIANO_STARTUP_MODE), None)
            or self.modes[0]
        )
        self.strip = Strip()

    def reconnect(self):
        if os.path.exists("/dev/midi"):
            self.midi_connection = mido.open_input(PIANO_MIDI_PORT)
            self.strip.startup_sequence()
            return True
        else:
            self.midi_connection = None
            time.sleep(PIANO_RECONNECT_TIMER)
            return False

    def is_connected(self):
        return self.midi_connection and os.path.exists("/dev/midi")

    def update_keyboard(self, msg):
        key = self.active_mode.keyboard.get(Key.index_to_name(msg.note))
        if msg.velocity > 0:
            key.set_hold(msg.velocity)
        else:
            key.set_released()
        return key

    def start_timer(self):
        self.access_settings_timer = time.time()

    def stop_timer(self):
        return time.time() - self.access_settings_timer

    def next_mode(self):
        for idx, mode in enumerate(self.modes):
            if mode == self.active_mode:
                self.active_mode = (
                    self.modes[idx + 1] if len(self.modes) > idx + 1 else self.modes[0]
                )
                break
        self.active_mode.show(self.strip)

    def process_input(self):
        for msg in self.midi_connection.iter_pending():
            if msg.type == "note_on":
                key = self.update_keyboard(msg)
                if key.note == PIANO_ACCESS_CONFIG_MODE_NOTE and key.is_pressed():
                    self.start_timer()
                if key.note == PIANO_ACCESS_CONFIG_MODE_NOTE and not key.is_pressed():
                    if self.stop_timer() > PIANO_ACCESS_SETTINGS_MODE_TIMER:
                        self.next_mode()
        self.active_mode.process(self.strip)
