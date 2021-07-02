from settings import *
from led import *
from strip import Strip

class ColorMode:
    def __init__(self, keyboard, active_keyboard, color_scheme, color_split_keys, touch_sensitive, fade_led, fade_speed):
        self.keyboard = keyboard
        self.active_keyboard = active_keyboard
        self.color_scheme = color_scheme
        self.color_split_keys = color_split_keys
        self.touch_sensitive = touch_sensitive
        self.fade_led = fade_led
        self.fade_speed = fade_speed

    @staticmethod
    def init_color_modes(keyboard, active_keyboard):
        modes = {
            'monochrome': 
            ColorMode(
                keyboard=keyboard,
                active_keyboard=active_keyboard,
                color_scheme=[Color.name('red')],
                color_split_keys=None,
                touch_sensitive=False,
                fade_led=True,
                fade_speed=0.95,
            ),
            'multicolor':
            ColorMode(
                keyboard=keyboard,
                active_keyboard=active_keyboard,
                color_scheme=[Color.name('red'), Color.name('blue')],
                color_split_keys=['C3'],
                touch_sensitive=False,
                fade_led=True,
                fade_speed=0.95,
            ),
            'multicolor-2':
            ColorMode(
                keyboard=keyboard,
                active_keyboard=active_keyboard,
                color_scheme=[Color.name('red'), Color.name('blue'), Color.name('green')],
                color_split_keys=['C3', 'C5'],
                touch_sensitive=False,
                fade_led=True,
                fade_speed=0.95,
            ),
            "rainbow":
            ColorMode(
                keyboard=keyboard,
                active_keyboard=active_keyboard,
                color_scheme=[Color.name('red')],
                color_split_keys=None,
                touch_sensitive=False,
                fade_led=True,
                fade_speed=0.95,
            )
        }

        return modes

    def init_leds(self):
        for index, (_, key) in enumerate(self.keyboard.items()):
            key.led = LED(
                Strip.get_led_index(index),
                velocity=100,
                touch_sensitive=self.touch_sensitive,
                fade_led=self.fade_led,
                fade_speed=self.fade_speed,
                default_color=self.color_scheme[0] #TODO Add Split possibilty
            )

    def process(self, strip):
        for _, key in list(self.active_keyboard.items()):
            if key.led.color:
                strip.setColor(key)
                key.led.process()
            else:
                self.active_keyboard.pop(key.name, None)