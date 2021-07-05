from settings import *
from led import *
from strip import Strip
from copy import deepcopy

class Mode:
    def __init__(self, name, keyboard, color_scheme, color_split_keys, touch_sensitive, fade_led, fade_speed):
        self.name = name
        self.keyboard = keyboard
        self.color_scheme = color_scheme
        self.color_split_keys = color_split_keys
        self.touch_sensitive = touch_sensitive
        self.fade_led = fade_led
        self.fade_speed = fade_speed

    @staticmethod
    def init_color_modes(keyboard):
        modes = {
            'monochrome': 
            Mode(
                name='monochrome',
                keyboard=deepcopy(keyboard),
                color_scheme=[Color.name('green')],
                color_split_keys=None,
                touch_sensitive=False,
                fade_led=True,
                fade_speed=0.95,
            ),
            'multicolor':
            Mode(
                name='multicolor',
                keyboard=deepcopy(keyboard),
                color_scheme=[Color.name('blue'), Color.name('red')],
                color_split_keys=['E3'],
                touch_sensitive=False,
                fade_led=True,
                fade_speed=0.95,
            ),
            'multicolor-2':
            Mode(
                name='multicolor-2',
                keyboard=deepcopy(keyboard),
                color_scheme=[Color.name('yellow'), Color.name('blue'), Color.name('green')],
                color_split_keys=['C3', 'C5'],
                touch_sensitive=False,
                fade_led=True,
                fade_speed=0.95,
            ),
            "rainbow":
            Mode(
                name='rainbow',
                keyboard=deepcopy(keyboard),
                color_scheme=Color.rainbow(),
                color_split_keys=PIANO_NOTES,
                touch_sensitive=False,
                fade_led=True,
                fade_speed=0.95,
            )
        }

        for _, mode in modes.items():
            mode.init_leds()

        return modes

    def init_leds(self):
        colors = []
        split_idx = 0
        color_idx = 0

        if self.color_split_keys:
            for _, (_, key) in enumerate(self.keyboard.items()):
                colors.append(self.color_scheme[color_idx])
                if key.name == self.color_split_keys[split_idx]:
                    if split_idx < len(self.color_split_keys) - 1:
                        split_idx += 1
                    color_idx += 1
                    continue
        else:
            for _, (_, key) in enumerate(self.keyboard.items()):
                colors.append(self.color_scheme[0])

        for index, (_, key) in enumerate(self.keyboard.items()):
            key.led = LED(
                Strip.get_led_index(index),
                touch_sensitive=self.touch_sensitive,
                fade_led=self.fade_led,
                fade_speed=self.fade_speed,
                default_color=colors[index]
            )

    def process(self, strip):
        for _, key in list(self.keyboard.items()):
            if key.led.color:
                strip.setColor(key)
                key.led.process()
        strip.show()