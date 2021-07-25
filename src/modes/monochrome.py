from settings import *
from led import *
from copy import deepcopy
from .abstract_mode import Mode
from state import State


class Monochrome(Mode):
    def __init__(self, keyboard):
        super().__init__("monochrome", deepcopy(keyboard))
        self.color_scheme = Color.name("green")
        self.color_split_keys = None
        self.fading = True
        self.init_leds()

    def init_leds(self):
        for _, key in self.keyboard.items():
            key.led = LED(
                fading=self.fading,
                default_color=self.color_scheme,
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
