import time
from midi import Midi
from multiprocessing import Queue
from piano.keyboard import Keyboard

from settings import (
    FUNC_TIMER_THRESHOLD,
    FUNCTIONS,
    MIDI_RECORD_LED_SIGNAL_KEY,
    PIANO_STARTUP_MODE,
)
from led_strip.strip import Strip
from led_strip.color import Color
from led_strip.color_schemes import Mono, Dual, Triple, Multi, Rainbow, CMajor
from .key import Key
from utility.state import KeyState, PianoState
from features.mic_analyzer import Analyzer
from features.record import Record
from features.playback import Playback


class Piano:
    def __init__(self, mic_analyze=True, midi_server=True):
        self.midi = Midi()
        self.strip = Strip()
        self.record = Record()
        self.state = PianoState.Default
        self.func_timer = 0
        self.playback_queue = Queue()
        self.color_schemes = [
            Mono(Keyboard()),
            Dual(Keyboard()),
            Triple(Keyboard()),
            Multi(Keyboard()),
            CMajor(Keyboard()),
            Rainbow(Keyboard()),
        ]
        if midi_server:
            self.midi.open_server()
        if mic_analyze:
            self.mic_analyze = Analyzer()
        self.active_color_scheme = (
            next((x for x in self.color_schemes if x.name == PIANO_STARTUP_MODE), None)
            or self.color_schemes[0]
        )

    def is_function_key(self, msg):
        if msg.type == "note_on":
            note = Keyboard.get_key_name_from_msg(msg)
            func_notes = [x["note"] for x in FUNCTIONS]
            return any(note == x for x in func_notes)
        else:
            return False

    def enable_led_force_control(self, keys):
        matching_keys = [x for x in self.active_color_scheme.keyboard.keys if x.note in keys]
        for key in matching_keys:
            key.led.force_control = True
            key.led.color = Color.name("red")

    def disable_led_force_control(self):
        for key in self.active_color_scheme.keyboard.keys:
            key.led.force_control = False
            key.led.color = None


    def cleanup_last_state(self):
        self.disable_led_force_control()
        self.record.stop()
        self.mic_analyze.stop()
        self.strip.clear()


    def handle_function_key(self, msg):
        key = self.active_color_scheme.get_key_from_msg(msg)
        if key.state == KeyState.Pressed:
            self.func_timer = time.time()

        elif key.state == KeyState.Released:
            threshold_exceeded = time.time() - self.func_timer > FUNC_TIMER_THRESHOLD
            func_name = [x["name"] for x in FUNCTIONS if x["note"] == key.note][0]

            if threshold_exceeded:
                self.cleanup_last_state()
                if func_name == "Switch to next mode":
                    self.mode = self.next_mode()

                if func_name == "Start/Stop Midi Recording":
                    if self.state != PianoState.Recording:
                        self.record.start()
                        self.enable_led_force_control([MIDI_RECORD_LED_SIGNAL_KEY])
                    self.state = (
                        PianoState.Recording
                        if not self.state == PianoState.Recording
                        else PianoState.Default
                    )

                if func_name == "Toggle Playback On/Off":
                    if self.state != PianoState.Playback:
                        self.playback = Playback(self.playback_queue)
                        self.playback.set_latest_file()
                        self.playback.start()
                        self.enable_led_force_control(["B7"])
                    self.state = (
                        PianoState.Playback
                        if not self.state == PianoState.Playback
                        else PianoState.Default
                    )

                if func_name == "Toggle Mic-Analyzer On/Off":
                    if self.mic_analyze:
                        if self.state != PianoState.MicAnalyze:
                            self.enable_led_force_control(["A7"])
                            self.mic_analyze.start(self.active_color_scheme.keyboard)
                        self.state = (
                            PianoState.MicAnalyze
                            if not self.state == PianoState.MicAnalyze
                            else PianoState.Default
                        )

                if func_name == "Toggle LEDs On/Off":
                    self.state = (
                        PianoState.LED_Off
                        if not self.state == PianoState.LED_Off
                        else PianoState.Default
                    )

                if func_name == "Set Background Light":
                    self.active_color_scheme.set_background_light_threshold()

    def update(self, msg):
        if msg.type == "note_on" or msg.type == "note_off":
            key = self.active_color_scheme.get_key_from_msg(msg)
            if key.state == KeyState.Released and msg.velocity > 0:
                key.set_pressed(msg.velocity)
            elif msg.velocity == 0:
                key.set_released(msg.velocity)
        elif msg.type == "control_change":
            self.active_color_scheme.sustain_pressed = (
                True if msg.value > 0 and msg.control == 64 else False
            )

    def next_mode(self):
        for idx, color_scheme in enumerate(self.color_schemes):
            if color_scheme == self.active_color_scheme:
                self.active_color_scheme = (
                    self.color_schemes[idx + 1] if len(self.color_schemes) > idx + 1 else self.color_schemes[0]
                )
                break
        self.active_color_scheme.show(self.strip)

    def process_forced_leds(self):
        for key in self.active_color_scheme.keyboard.get_force_controlled_keys():
            key.led.color.pulse()

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

                if self.state == PianoState.Recording:
                    self.record.process(msg)

            if self.state == PianoState.Playback:
                if not self.playback_queue.empty():
                    msg = self.playback_queue.get(block=False)
                if msg:
                    self.midi.output_port.send(msg)
                    self.update(msg)

            if self.state == PianoState.MicAnalyze:
                self.mic_analyze.process(self.strip)

        if not self.state == PianoState.LED_Off:
            self.active_color_scheme.process(self.strip)

        
        self.process_forced_leds()