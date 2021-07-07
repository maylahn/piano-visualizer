from settings import *
from led import *
from copy import deepcopy
from .abstract_mode import Mode


class Monochrome(Mode):
    def __init__(self, keyboard):
        super().__init__("monochrome", deepcopy(keyboard))
        self.color_scheme = Color.name("green")
        self.color_split_keys = None
        self.touch_sensitive = False
        self.fade_led = True
        self.fade_speed = 0.95
        self.init_leds()

    def init_leds(self):
        for index, (_, key) in enumerate(self.keyboard.items()):
            key.led = LED(
                key.get_led_index(index),
                touch_sensitive=self.touch_sensitive,
                fade_led=self.fade_led,
                fade_speed=self.fade_speed,
                default_color=self.color_scheme,
            )

    def process(self, strip):
        for _, key in list(self.keyboard.items()):
            if key.led.color:
                strip.set_pixel_color(key.led)
                key.led.process()
        strip.show()
