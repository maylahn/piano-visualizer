import os
import mido
import time
import datetime

from settings import (
    PIANO_STARTUP_MODE,
    PIANO_MIDI_PORT,
    PIANO_RECONNECT_TIMER,
    PIANO_NEXT_MODE_NOTE,
    PIANO_NEXT_MODE_TIMER,
    PIANO_RECORD_MIDI_NOTE,
    PIANO_RECORD_MIDI_TIMER,
    MIDI_TEMPO_MULTIPLIER,
    MIDI_SAVE_DIRECTORY,
    MIDI_SAVE_TIME_FORMAT,
)
from strip import Strip
from modes import basics, fft, explode
from key import Key
from state import State
from color import Color
from pathlib import Path


class Piano:
    def __init__(self, fft_mode=True):
        self.timer_record_midi = None
        self.timer_next_mode = None
        self.midi_tempo = None
        self.midi_connection = None
        self.keyboard = Key.init_keyboard()
        self.modes = [
            basics.Mono(self.keyboard),
            basics.Dual(self.keyboard),
            basics.Triple(self.keyboard),
            basics.Multi(self.keyboard),
            basics.CMajor(self.keyboard),
            basics.Rainbow(self.keyboard),
            explode.Explode(self.keyboard),
        ]
        if fft_mode:
            self.modes += [fft.FFT(self.keyboard)]
        self.active_mode = (
            next((mode for mode in self.modes if mode.name == PIANO_STARTUP_MODE), None)
            or self.modes[0]
        )
        self.strip = Strip()
        self.recording = False
        self.active_mode.show(self.strip)

    def reconnect(self):
        if os.path.exists("/dev/midi"):
            self.midi_connection = mido.open_input(PIANO_MIDI_PORT)
            self.active_mode.show(self.strip)
            return True
        else:
            self.midi_connection = None
            time.sleep(PIANO_RECONNECT_TIMER)
            return False

    def is_connected(self):
        return self.midi_connection and os.path.exists("/dev/midi")

    def update_state(self, msg):
        key = self.active_mode.keyboard.get(Key.index_to_name(msg.note))
        if key.state == State.Released and msg.velocity > 0:
            key.set_pressed(msg.velocity)
        elif msg.velocity == 0:
            key.set_released(msg.velocity)
        return key

    def next_mode(self):
        if self.active_mode.name == "fft":
            self.active_mode.stop_audio()

        for idx, mode in enumerate(self.modes):
            if mode == self.active_mode:
                self.active_mode = (
                    self.modes[idx + 1] if len(self.modes) > idx + 1 else self.modes[0]
                )
                break
        self.active_mode.show(self.strip)
        if self.active_mode.name == "fft":
            self.active_mode.start_audio()

    def toggle_record_midi(self):
        if self.is_recording():
            self.active_mode.keyboard[PIANO_RECORD_MIDI_NOTE].led.force_control = False
            self.active_mode.keyboard[PIANO_RECORD_MIDI_NOTE].led.color = None
            del self.track[0]
            del self.track[-1]
            Path(MIDI_SAVE_DIRECTORY).mkdir(parents=True, exist_ok=True)
            filename = "{}/{}.mid".format(
                MIDI_SAVE_DIRECTORY,
                datetime.datetime.now().strftime(MIDI_SAVE_TIME_FORMAT),
            )
            self.midi.save(filename=filename)
            self.strip.clear()
        else:
            self.active_mode.keyboard[PIANO_RECORD_MIDI_NOTE].led.force_control = True
            self.active_mode.keyboard[PIANO_RECORD_MIDI_NOTE].led.color = Color.name(
                "red"
            )
            self.midi = mido.MidiFile()
            self.track = mido.MidiTrack()
            self.midi_tempo = time.time()
            self.midi.tracks.append(self.track)
        self.recording = not self.recording

    def update_timer(self, key):
        if key.note == PIANO_NEXT_MODE_NOTE and key.state == State.Pressed:
            self.timer_next_mode = time.time()
        if (
            key.note == PIANO_RECORD_MIDI_NOTE
            and key.state == State.Pressed
            and not self.is_recording()
        ):
            self.timer_record_midi = time.time()

    def check_next_mode(self, key):
        return (
            key.note == PIANO_NEXT_MODE_NOTE
            and key.state == State.Released
            and time.time() - self.timer_next_mode > PIANO_NEXT_MODE_TIMER
            and not self.recording
        )

    def check_toggle_record_midi(self, key):
        return (
            key.note == PIANO_RECORD_MIDI_NOTE
            and key.state == State.Released
            and time.time() - self.timer_record_midi > PIANO_RECORD_MIDI_TIMER
        )

    def update_sustain(self, msg):
        self.active_mode.sustain_pressed = (
            True if msg.value > 0 and msg.control == 64 else False
        )

    def process_forced_leds(self):
        if self.is_recording():
            self.active_mode.keyboard[PIANO_RECORD_MIDI_NOTE].led.color.pulse()

    def is_recording(self):
        return self.recording

    def recording_add_sustain(self, msg):
        self.track.append(
            mido.Message(
                "control_change",
                control=64,
                value=msg.value,
                time=int((time.time() - self.midi_tempo) * MIDI_TEMPO_MULTIPLIER),
            )
        )
        self.midi_tempo = time.time()

    def recording_add_key(self, msg):
        type = "note_on" if msg.velocity > 0 else "note_off"
        self.track.append(
            mido.Message(
                type,
                note=msg.note,
                velocity=msg.velocity,
                time=int((time.time() - self.midi_tempo) * MIDI_TEMPO_MULTIPLIER),
            )
        )
        self.midi_tempo = time.time()

    def process_input(self):
        for msg in self.midi_connection.iter_pending():
            if msg.type == "control_change":
                self.update_sustain(msg)
                if self.is_recording():
                    self.recording_add_sustain(msg)

            if msg.type == "note_on":
                key = self.update_state(msg)
                self.update_timer(key)
                if self.check_next_mode(key):
                    self.next_mode()
                if self.check_toggle_record_midi(key):
                    self.toggle_record_midi()
                if self.is_recording():
                    self.recording_add_key(msg)

        self.process_forced_leds()
        self.active_mode.process(self.strip)
