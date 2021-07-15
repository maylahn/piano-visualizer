from settings import *
from led import *
from copy import deepcopy
from .abstract_mode import Mode
from state import State


class FFT(Mode):
    def __init__(self, keyboard, audio):
        super().__init__("fft", deepcopy(keyboard))
        self.color_scheme = Color.name("red")
        self.fade_led = False
        self.fade_speed = 0.5
        self.audio = audio
        self.init_leds()

    def init_leds(self):
        for _, key in self.keyboard.items():
            key.led = LED(
                fade_led=self.fade_led,
                fade_speed=self.fade_speed,
                default_color=self.color_scheme,
            )

    def process(self, strip):
        freq = self.audio.get_frequency()
        for _, key in self.keyboard.items():
            if key.frequency == freq:
                key.state = State.Pressed
                key.led.set_color()
                key.state = State.Released
            elif key.state == State.Released and key.led.color:
                key.led.process()
        strip.set_color(self.keyboard)
        strip.show()
