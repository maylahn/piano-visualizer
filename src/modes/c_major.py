from settings import *
from led import *
from copy import deepcopy
from .abstract_mode import Mode


class cMajor(Mode):
    def __init__(self, keyboard):
        super().__init__("c_major", deepcopy(keyboard))
        self.color_scheme = [
            Color.random(),
            Color.random(),
            Color.random(),
            Color.random(),
            Color.random(),
            Color.random(),
            Color.random(),
            Color.random(),
            Color.random(),
        ]
        self.color_split_keys = ["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8"]
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
