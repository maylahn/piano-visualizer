import mido
import time

from settings import (
    FUNC_TIMER_THRESHOLD,
    FUNCTIONS,
    MIDI_RECORD_LED_SIGNAL_KEY,
    PIANO_STARTUP_MODE,
)
from strip import Strip
from modes.basics import Mono, Dual, Triple, Multi, Rainbow, CMajor
from modes.explode import Explode
from modes.fft import FFT
from key import Key
from state import KeyState, PianoState
from color import Color
from pathlib import Path
from midi import Midi


class Piano:
    def __init__(self, fft_mode=True, midi_server=True):
        self.midi = Midi()
        self.keyboard = Key.init_keyboard()
        self.strip = Strip()
        self.state = PianoState.Default
        self.modes = [
            Mono(self.keyboard),
            Dual(self.keyboard),
            Triple(self.keyboard),
            Multi(self.keyboard),
            CMajor(self.keyboard),
            Rainbow(self.keyboard),
            Explode(self.keyboard),
        ]
        if midi_server:
            self.midi.open_server()
        if fft_mode:
            self.modes += [FFT(self.keyboard)]
        self.active_mode = (
            next((mode for mode in self.modes if mode.name == PIANO_STARTUP_MODE), None)
            or self.modes[0]
        )

    def get_key(self, msg):
        return self.active_mode.keyboard.get(Key.index_to_name(msg.note))

    def is_function_key(self, msg):
        if msg.type == "note_on":
            note = Key.index_to_name(msg.note)
            func_notes = [x['note'] for x in FUNCTIONS]
            return any(note==x for x in func_notes)
        else:
            return False

    def handle_function_key(self, msg):
        key = self.get_key(msg)
        if key.state == KeyState.Pressed:
            self.func_timer = time.time()

        elif key.state == KeyState.Released:
            threshold_exceeded = time.time() - self.func_timer > FUNC_TIMER_THRESHOLD
            func_name = [x["name"] for x in FUNCTIONS if x["note"] == key.note][0]

            if threshold_exceeded:
                if func_name == "Switch to next mode":
                    self.mode = self.next_mode()

                if func_name == "Start/Stop Midi Recording":
                    if self.state != PianoState.Recording:
                        self.midi.start_recording()
                        self.active_mode.keyboard[MIDI_RECORD_LED_SIGNAL_KEY].led.force_control = True
                        self.active_mode.keyboard[MIDI_RECORD_LED_SIGNAL_KEY].led.color = Color.name(
                            "red"
                        )
                    else:
                        self.midi.stop_recording()
                        self.active_mode.keyboard[MIDI_RECORD_LED_SIGNAL_KEY].led.force_control = False
                        self.active_mode.keyboard[MIDI_RECORD_LED_SIGNAL_KEY].led.color = None
                        self.strip.clear()
                    self.state = PianoState.Recording if not self.state == PianoState.Recording else PianoState.Default

                if func_name == "Toggle Playback On/Off":
                    self.state = PianoState.Playback if not self.state == PianoState.Playback else PianoState.Default


                if func_name == "Toggle FFT-Mode On/Off":
                    if self.state != PianoState.FFT:
                        pass
                    self.state = PianoState.FFT if not self.state == PianoState.FFT else PianoState.Default

                if func_name == "Toggle LEDs On/Off":
                    self.state = PianoState.LED_Off if not self.state == PianoState.LED_Off else PianoState.Default

    def update(self, msg):
        if msg.type == "note_on":
            key = self.get_key(msg)
            if key.state == KeyState.Released and msg.velocity > 0:
                key.set_pressed(msg.velocity)
            elif msg.velocity == 0:
                key.set_released(msg.velocity)
        elif msg.type == "control_change":
            self.active_mode.sustain_pressed = (
                True if msg.value > 0 and msg.control == 64 else False
            )

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

    def process_forced_leds(self):
        leds = [key.led for key in self.active_mode.keyboard.values() if key.led.force_control]
        for led in leds:
            led.color.pulse()

    def process_input(self):
        for msg in self.midi.input_port.iter_pending():
            if msg.type == "control_change" or msg.type == "note_on":
                # Send msg to tcp/ip clients
                self.midi.check_connection()
                self.midi.send(msg)
                self.update(msg)

                # Check if any function is associated with the key
                if self.is_function_key(msg):
                    self.handle_function_key(msg)

                # Handle messages depending on current state
                if self.state == PianoState.Default:
                    pass

                if self.state == PianoState.Recording:
                    self.midi.add_to_file(msg)
                    
                if self.state == PianoState.Playback:
                    pass

                if self.state == PianoState.FFT:
                    pass

                if self.state == PianoState.LED_Off:
                    pass

        self.process_forced_leds()
        self.active_mode.process(self.strip)
