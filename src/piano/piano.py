import time
from midi import Midi
from piano.keyboard import Keyboard

from settings import (
    FUNC_TIMER_THRESHOLD,
    FUNCTIONS,
    PIANO_STARTUP_MODE,
)
from led_strip.strip import Strip
from led_strip.color import Color
from led_strip.color_schemes import Mono, Dual, Triple, Multi, Rainbow, CMajor
from utility.state import KeyState, PianoState
from features.mic_analyzer import AnalyzerHandler
from features.record import RecordHandler
from features.playback import PlaybackHandler


class Piano:
    def __init__(self, mic_analyze=True, midi_server=True):
        self.state = PianoState.Default
        self.midi = Midi()
        self.strip = Strip()
        self.record = RecordHandler()
        self.playback = PlaybackHandler()
        self.mic_analyze = AnalyzerHandler() if mic_analyze else None
        self.color_schemes = self.init_color_schemes()
        self.func_timer = 0
        self.midi.open_server() if midi_server else None
        self.active_color_scheme = self.init_startup_color_scheme()

    def init_startup_color_scheme(self):
        return (
            next((x for x in self.color_schemes if x.name == PIANO_STARTUP_MODE), None)
            or self.color_schemes[0]
        )

    def init_color_schemes(self):
        return [
            Mono(Keyboard()),
            Dual(Keyboard()),
            Triple(Keyboard()),
            Multi(Keyboard()),
            CMajor(Keyboard()),
            Rainbow(Keyboard()),
        ]

    def is_function_key(self, msg):
        if msg.type == "note_on":
            note = Keyboard.get_key_name_from_msg(msg)
            func_notes = [x["note"] for x in FUNCTIONS]
            return any(note == x for x in func_notes)
        else:
            return False

    def enable_led_force_control(self, indicator):
        key = self.active_color_scheme.keyboard.get_key_from_note(indicator["note"])
        key.led.force_control = True
        key.led.default_color = Color.name(indicator["color"])
        # key.led.type? = indicator['type']

    def disable_led_force_control(self):
        for key in self.active_color_scheme.keyboard.keys:
            key.led.force_control = False
            key.led.color = None

    def cleanup_last_state(self):
        self.disable_led_force_control()
        self.record.stop()
        self.mic_analyze.stop()
        self.playback.stop()
        self.strip.clear()

    def change_state(self, function):
        self.cleanup_last_state()

        if function["name"] == "Switch to next mode":
            self.mode = self.next_mode()

        if function["name"] == "Start/Stop Midi Recording":
            if self.state != PianoState.Recording:
                self.record.start()
                self.enable_led_force_control(function["indicator"])
            self.state = (
                PianoState.Recording
                if not self.state == PianoState.Recording
                else PianoState.Default
            )

        if function["name"] == "Toggle Playback On/Off":
            if self.state != PianoState.Playback:
                self.playback.set_latest_file()
                self.playback.start()
                self.enable_led_force_control(function["indicator"])
            self.state = (
                PianoState.Playback
                if not self.state == PianoState.Playback
                else PianoState.Default
            )

        if function["name"] == "Toggle Mic-Analyzer On/Off":
            if self.mic_analyze:
                if self.state != PianoState.MicAnalyze:
                    self.enable_led_force_control(function["indicator"])
                    self.mic_analyze.start(self.active_color_scheme.keyboard)
                self.state = (
                    PianoState.MicAnalyze
                    if not self.state == PianoState.MicAnalyze
                    else PianoState.Default
                )

        if function["name"] == "Toggle LEDs On/Off":
            self.state = (
                PianoState.LED_Off
                if not self.state == PianoState.LED_Off
                else PianoState.Default
            )

        if function["name"] == "Set Background Light":
            self.active_color_scheme.set_background_light_threshold()
            self.active_color_scheme.show_activate_sequence(self.strip)

    def handle_function_key(self, msg):
        key = self.active_color_scheme.get_key_from_msg(msg)
        if key.state == KeyState.Pressed:
            self.func_timer = time.time()

        elif key.state == KeyState.Released:
            threshold_exceeded = time.time() - self.func_timer > FUNC_TIMER_THRESHOLD
            function = [x for x in FUNCTIONS if x["note"] == key.note][0]

            if threshold_exceeded:
                self.change_state(function)

    def update(self, msg):
        if msg.type == "note_on" or msg.type == "note_off":
            key = self.active_color_scheme.get_key_from_msg(msg)
            if msg.type == "note_on":
                if msg.velocity > 0:
                    key.set_pressed(msg.velocity)
                if msg.velocity == 0:
                    key.set_released()
            if msg.type == "note_off":
                key.set_released()
        elif msg.type == "control_change":
            self.active_color_scheme.sustain_pressed = (
                True if msg.value > 0 and msg.control == 64 else False
            )

    def next_mode(self):
        for idx, color_scheme in enumerate(self.color_schemes):
            if color_scheme == self.active_color_scheme:
                self.active_color_scheme = (
                    self.color_schemes[idx + 1]
                    if len(self.color_schemes) > idx + 1
                    else self.color_schemes[0]
                )
                break
        self.active_color_scheme.show_activate_sequence(self.strip)

    def process_forced_leds(self):
        for key in self.active_color_scheme.keyboard.get_force_controlled_keys():
            key.led.process_forced()

    def process_input(self):
        for msg in self.midi.input_port.iter_pending():
            if msg.type == "control_change" or msg.type == "note_on":
                # Send msg to tcp/ip clients
                if self.midi.server:
                    self.midi.check_connection()
                    self.midi.send(msg)
                self.update(msg)

                # Check if any function is associated with the key
                if self.is_function_key(msg):
                    self.handle_function_key(msg)

                if self.state == PianoState.Recording:
                    self.record.process(msg)

        if self.state == PianoState.Playback:
            msg = self.playback.process(self.midi.output_port)
            if msg:
                if msg.is_meta:
                    self.change_state(
                        [x for x in FUNCTIONS if x["name"] == "Toggle Playback On/Off"][
                            0
                        ]
                    )
                else:
                    self.update(msg)

        if self.state == PianoState.MicAnalyze:
            msg = self.mic_analyze.process()
            if msg:
                self.update(msg)

        if not self.state == PianoState.LED_Off:
            self.active_color_scheme.process(self.strip)

        self.process_forced_leds()
