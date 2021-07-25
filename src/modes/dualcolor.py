from settings import *
from led import *
from copy import deepcopy
from .abstract_mode import Mode
from state import State


class Dualcolor(Mode):
    def __init__(self, keyboard):
        super().__init__("dualcolor", deepcopy(keyboard))
        self.color_scheme = [Color.name("blue"), Color.name("red")]
        self.color_split_keys = ["E3"]
        self.fading = True
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
                fading=self.fading,
                default_color=colors[index],
            )

    def process(self, strip):
        for _, key in self.keyboard.items():
            if key.state == State.Pressed:
                key.state = State.Hold
                key.led.set_color()
            if key.state == State.Released and key.led.color:
                key.led.process(self.sustain)
        strip.set_color(self.keyboard)
        strip.show()
