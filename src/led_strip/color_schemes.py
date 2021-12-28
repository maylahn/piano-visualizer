from settings import LED_BACKGROUND_LIGHT_THRESHOLD
from led_strip.led import LED
from led_strip.color import Color
from led_strip.sequences import Sequence
from copy import deepcopy
from time import sleep
from utility.state import KeyState


class Scheme:
    def __init__(self, name, keyboard):
        self.name = name
        self.keyboard = keyboard
        self.sustain_pressed = False
        self.fading = True
        self.velocity = True
        self.sequence = Sequence("X")
        self.background_light_threshold = LED_BACKGROUND_LIGHT_THRESHOLD
        self.color_key_mapping = {
            "A0": Color.name("white"),
        }

    def init_leds(self):
        color = self.color_key_mapping.get("A0", Color.name("white"))

        for key in self.keyboard.keys:
            color = self.color_key_mapping.get(key.note, color)
            key.led = LED(
                fading=self.fading,
                default_color=color,
                background_light_threshold=self.background_light_threshold,
            )

    def get_key_from_msg(self, msg):
        return self.keyboard.get_key_from_msg(msg)

    def set_background_light_threshold(self):
        self.background_light_threshold = (
            self.background_light_threshold + 3
            if self.background_light_threshold < 9
            else 0
        )

        for key in self.keyboard.keys:
            key.led.background_light_threshold = self.background_light_threshold

    def show_activate_sequence(self, strip):
        self.sequence.show(strip, self.keyboard)

    def process(self, strip):
        for key in self.keyboard.keys:
            if key.state == KeyState.Pressed:
                key.state = KeyState.Hold
                if self.velocity:
                    key.led.set_color(velocity=key.velocity)
                else:
                    key.led.set_color()
            if key.state == KeyState.Released and key.led.color:
                key.led.process(self.sustain_pressed)
        strip.set_color(self.keyboard)
        strip.show()


class Mono(Scheme):
    def __init__(self, keyboard):
        super().__init__("mono", deepcopy(keyboard))
        self.color_key_mapping = {
            "A0": Color.name("blue"),
        }
        self.init_leds()


class Dual(Scheme):
    def __init__(self, keyboard):
        super().__init__("dual", deepcopy(keyboard))
        self.color_key_mapping = {"A0": Color.name("blue"), "C3": Color.name("red")}
        self.init_leds()


class Triple(Scheme):
    def __init__(self, keyboard):
        super().__init__("triple", deepcopy(keyboard))
        self.color_key_mapping = {
            "A0": Color.name("blue"),
            "C3": Color.name("red"),
            "C5": Color.name("green"),
        }
        self.init_leds()


class Multi(Scheme):
    def __init__(self, keyboard):
        super().__init__("multi", deepcopy(keyboard))
        self.color_key_mapping = {
            "A0": Color.name("blue"),
            "C3": Color.name("red"),
            "C5": Color.name("green"),
            "C7": Color.name("yellow"),
        }
        self.init_leds()


class CMajor(Scheme):
    def __init__(self, keyboard):
        super().__init__("cmajor", deepcopy(keyboard))
        self.color_key_mapping = {
            "C0": Color.name("blue"),
            "C1": Color.name("red"),
            "C2": Color.name("green"),
            "C3": Color.name("yellow"),
            "C4": Color.name("cyan"),
            "C5": Color.name("magenta"),
            "C6": Color.name("lime"),
            "C7": Color.name("silver"),
            "C8": Color.name("navy"),
        }
        self.init_leds()


class Rainbow(Scheme):
    def __init__(self, keyboard):
        super().__init__("rainbow", deepcopy(keyboard))
        self.color_key_mapping = {
            "A0": Color.hex("ff0000"),
            "A#0": Color.hex("ff0d00"),
            "B0": Color.hex("ff1e00"),
            "C1": Color.hex("ff2b00"),
            "C#1": Color.hex("ff3c00"),
            "D1": Color.hex("ff4800"),
            "D#1": Color.hex("ff5900"),
            "E1": Color.hex("ff6600"),
            "F1": Color.hex("ff7700"),
            "F#1": Color.hex("ff8400"),
            "G1": Color.hex("ff9100"),
            "G#1": Color.hex("ffa200"),
            "A1": Color.hex("ffae00"),
            "A#1": Color.hex("ffbf00"),
            "B1": Color.hex("ffcc00"),
            "C2": Color.hex("ffdd00"),
            "C#2": Color.hex("ffea00"),
            "D2": Color.hex("fffb00"),
            "D#2": Color.hex("f7ff00"),
            "E2": Color.hex("e6ff00"),
            "F2": Color.hex("d9ff00"),
            "F#2": Color.hex("ccff00"),
            "G2": Color.hex("bbff00"),
            "G#2": Color.hex("aeff00"),
            "A2": Color.hex("9dff00"),
            "A#2": Color.hex("91ff00"),
            "B2": Color.hex("80ff00"),
            "C3": Color.hex("73ff00"),
            "C#3": Color.hex("62ff00"),
            "D3": Color.hex("55ff00"),
            "D#3": Color.hex("48ff00"),
            "E3": Color.hex("37ff00"),
            "F3": Color.hex("2bff00"),
            "F#3": Color.hex("1aff00"),
            "G3": Color.hex("0dff00"),
            "G#3": Color.hex("00ff04"),
            "A3": Color.hex("00ff11"),
            "A#3": Color.hex("00ff22"),
            "B3": Color.hex("00ff2f"),
            "C4": Color.hex("00ff3c"),
            "C#4": Color.hex("00ff4d"),
            "D4": Color.hex("00ff59"),
            "D#4": Color.hex("00ff6a"),
            "E4": Color.hex("00ff77"),
            "F4": Color.hex("00ff88"),
            "F#4": Color.hex("00ff95"),
            "G4": Color.hex("00ffa6"),
            "G#4": Color.hex("00ffb3"),
            "A4": Color.hex("00ffc4"),
            "A#4": Color.hex("00ffd0"),
            "B4": Color.hex("00ffdd"),
            "C5": Color.hex("00ffee"),
            "C#5": Color.hex("00fffb"),
            "D5": Color.hex("00f2ff"),
            "D#5": Color.hex("00e6ff"),
            "E5": Color.hex("00d5ff"),
            "F5": Color.hex("00c8ff"),
            "F#5": Color.hex("00b7ff"),
            "G5": Color.hex("00aaff"),
            "G#5": Color.hex("009dff"),
            "A5": Color.hex("008cff"),
            "A#5": Color.hex("0080ff"),
            "B5": Color.hex("006fff"),
            "C6": Color.hex("0062ff"),
            "C#6": Color.hex("0051ff"),
            "D6": Color.hex("0044ff"),
            "D#6": Color.hex("0033ff"),
            "E6": Color.hex("0026ff"),
            "F6": Color.hex("001aff"),
            "F#6": Color.hex("0009ff"),
            "G6": Color.hex("0400ff"),
            "G#6": Color.hex("1500ff"),
            "A6": Color.hex("2200ff"),
            "A#6": Color.hex("3300ff"),
            "B6": Color.hex("4000ff"),
            "C7": Color.hex("5100ff"),
            "C#7": Color.hex("5e00ff"),
            "D7": Color.hex("6f00ff"),
            "D#7": Color.hex("7b00ff"),
            "E7": Color.hex("8800ff"),
            "F7": Color.hex("9900ff"),
            "F#7": Color.hex("a600ff"),
            "G7": Color.hex("b700ff"),
            "G#7": Color.hex("c400ff"),
            "A7": Color.hex("d500ff"),
            "A#7": Color.hex("e100ff"),
            "B7": Color.hex("f200ff"),
            "C8": Color.hex("ff00ff"),
        }
        self.init_leds()
