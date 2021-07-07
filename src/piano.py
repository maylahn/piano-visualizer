import os
import mido
import time

from copy import deepcopy
from settings import *
from strip import Strip
from audio import Audio
from mode import Mode
from config_mode import ConfigMode
from key import Key

class Piano:

    def __init__(self, mic_active=True):
        self.access_settings_timer = None
        self.midi_connection = None
        if mic_active:
            self.audio = Audio()
        self.keyboard = Key.init_keys()
        self.modes = Mode.init_color_modes(self.keyboard, self.audio)
        self.config_mode = ConfigMode()
        self.active_mode = self.modes[PIANO_STARTUP_MODE] or self.modes['monochrome']

        self.strip = Strip()

    def reconnect(self):
        if os.path.exists("/dev/midi"):
            self.midi_connection = mido.open_input(PIANO_MIDI_PORT)
            return True
        else:
            self.midi_connection = None
            time.sleep(PIANO_RECONNECT_TIMER)
            return False

    def is_connected(self):
        return self.midi_connection and os.path.exists("/dev/midi")

    def update_key(self, msg):
        key = self.active_mode.keyboard.get(Key.index_to_name(msg.note))
        if not self.active_mode.name == 'fft':
            if msg.velocity > 0 :
                key.set_pressed(msg.velocity)
            else:
                key.set_released(msg.velocity)
        return key

    def start_timer(self):
        self.access_settings_timer = time.process_time()

    def stop_timer(self):
        return time.process_time() - self.access_settings_timer

    def process_input(self):
        for msg in self.midi_connection.iter_pending():
            if msg.type == "note_on":
                key = self.update_key(msg)
                if key.name == PIANO_ACCESS_CONFIG_MODE_NOTE and key.is_pressed():
                    self.start_timer()
                if key.name == PIANO_ACCESS_CONFIG_MODE_NOTE and not key.is_pressed():
                    if self.stop_timer() > PIANO_ACCESS_SETTINGS_MODE_TIMER:
                        self.config_mode.toggle()

        if self.config_mode.is_active():
            pass
            #self.config_mode.process(self.strip, note)
        else:
            self.active_mode.process(self.strip)
