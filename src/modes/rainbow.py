from settings import *
from led import *
from copy import deepcopy
from .abstract_mode import Mode


class Rainbow(Mode):
    rainbow_colors = [
        Color.hex("ff0000"),
        Color.hex("ff0d00"),
        Color.hex("ff1e00"),
        Color.hex("ff2b00"),
        Color.hex("ff3c00"),
        Color.hex("ff4800"),
        Color.hex("ff5900"),
        Color.hex("ff6600"),
        Color.hex("ff7700"),
        Color.hex("ff8400"),
        Color.hex("ff9100"),
        Color.hex("ffa200"),
        Color.hex("ffae00"),
        Color.hex("ffbf00"),
        Color.hex("ffcc00"),
        Color.hex("ffdd00"),
        Color.hex("ffea00"),
        Color.hex("fffb00"),
        Color.hex("f7ff00"),
        Color.hex("e6ff00"),
        Color.hex("d9ff00"),
        Color.hex("ccff00"),
        Color.hex("bbff00"),
        Color.hex("aeff00"),
        Color.hex("9dff00"),
        Color.hex("91ff00"),
        Color.hex("80ff00"),
        Color.hex("73ff00"),
        Color.hex("62ff00"),
        Color.hex("55ff00"),
        Color.hex("48ff00"),
        Color.hex("37ff00"),
        Color.hex("2bff00"),
        Color.hex("1aff00"),
        Color.hex("0dff00"),
        Color.hex("00ff04"),
        Color.hex("00ff11"),
        Color.hex("00ff22"),
        Color.hex("00ff2f"),
        Color.hex("00ff3c"),
        Color.hex("00ff4d"),
        Color.hex("00ff59"),
        Color.hex("00ff6a"),
        Color.hex("00ff77"),
        Color.hex("00ff88"),
        Color.hex("00ff95"),
        Color.hex("00ffa6"),
        Color.hex("00ffb3"),
        Color.hex("00ffc4"),
        Color.hex("00ffd0"),
        Color.hex("00ffdd"),
        Color.hex("00ffee"),
        Color.hex("00fffb"),
        Color.hex("00f2ff"),
        Color.hex("00e6ff"),
        Color.hex("00d5ff"),
        Color.hex("00c8ff"),
        Color.hex("00b7ff"),
        Color.hex("00aaff"),
        Color.hex("009dff"),
        Color.hex("008cff"),
        Color.hex("0080ff"),
        Color.hex("006fff"),
        Color.hex("0062ff"),
        Color.hex("0051ff"),
        Color.hex("0044ff"),
        Color.hex("0033ff"),
        Color.hex("0026ff"),
        Color.hex("001aff"),
        Color.hex("0009ff"),
        Color.hex("0400ff"),
        Color.hex("1500ff"),
        Color.hex("2200ff"),
        Color.hex("3300ff"),
        Color.hex("4000ff"),
        Color.hex("5100ff"),
        Color.hex("5e00ff"),
        Color.hex("6f00ff"),
        Color.hex("7b00ff"),
        Color.hex("8800ff"),
        Color.hex("9900ff"),
        Color.hex("a600ff"),
        Color.hex("b700ff"),
        Color.hex("c400ff"),
        Color.hex("d500ff"),
        Color.hex("e100ff"),
        Color.hex("f200ff"),
        Color.hex("ff00ff"),
    ]

    def __init__(self, keyboard):
        super().__init__("rainbow", deepcopy(keyboard))
        self.color_scheme = self.rainbow_colors
        self.color_split_keys = PIANO_NOTES
        self.touch_sensitive = False
        self.fade_led = True
        self.fade_speed = 0.95
        self.init_leds()

    def init_leds(self):
        colors = []
        split_idx = 0
        color_idx = 0

        for _, (_, key) in enumerate(self.keyboard.items()):
            colors.append(self.color_scheme[color_idx])
            if key.note == self.color_split_keys[split_idx]:
                if split_idx < len(self.color_split_keys) - 1:
                    split_idx += 1
                color_idx += 1
                continue

        for index, (_, key) in enumerate(self.keyboard.items()):
            key.led = LED(
                key.get_led_index(index),
                touch_sensitive=self.touch_sensitive,
                fade_led=self.fade_led,
                fade_speed=self.fade_speed,
                default_color=colors[index],
            )

    def process(self, strip):
        for _, key in list(self.keyboard.items()):
            if key.led.color:
                strip.set_pixel_color(key.led)
                key.led.process()
        strip.show()