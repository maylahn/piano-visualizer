from settings import *
from led import *
from strip import Strip
from copy import deepcopy
from .abstract_mode import Mode


class Multicolor(Mode):
    def __init__(self, keyboard):
        super().__init__("multicolor", deepcopy(keyboard))
        self.color_scheme = [
            Color.name("yellow"),
            Color.name("blue"),
            Color.name("green"),
        ]
        self.color_split_keys = ["C3", "C5"]
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
                strip.setColor(key)
                key.led.process()
        strip.show()
