from settings import *
from led import *
from copy import deepcopy
from .abstract_mode import Mode
from state import State


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
        self.fade_led = True
        self.fade_speed = 0.95
        self.init_leds()

    def init_leds(self):
        colors = []
        split_idx = 0
        color_idx = 0

        for _, key in self.keyboard.items():
            colors.append(self.color_scheme[color_idx])
            if key.note == self.color_split_keys[split_idx]:
                if split_idx < len(self.color_split_keys) - 1:
                    split_idx += 1
                color_idx += 1
                continue

        for index, (_, key) in enumerate(self.keyboard.items()):
            key.led = LED(
                fade_led=self.fade_led,
                fade_speed=self.fade_speed,
                default_color=colors[index],
            )

    def process(self, strip):
        for _, key in self.keyboard.items():
            if key.state == State.Pressed:
                key.state = State.Hold
                key.led.set_color()
            if key.state == State.Released and key.led.color:
                key.led.process()
        strip.set_color(self.keyboard)
        strip.show()
