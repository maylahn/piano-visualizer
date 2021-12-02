import time
from color import Color

from led import LED
from state import State


class Mode:
    def __init__(self, name, keyboard):
        self.name = name
        self.keyboard = keyboard
        self.sustain_pressed = False
        self.fading = True
        self.velocity = True
        self.color_key_mapping = {
            "A0": Color.name("white"),
        }

    def init_leds(self):
        color = self.color_key_mapping.get("A0", Color.name("white"))

        for note, key in self.keyboard.items():
            color = self.color_key_mapping.get(note, color)
            key.led = LED(
                fading=self.fading,
                default_color=color,
            )

    def show(self, strip, timer=1):
        strip.clear()
        for _, key in self.keyboard.items():
            key.set_pressed()
            key.led.set_color(velocity=50)
        strip.set_color(self.keyboard)
        strip.show()
        time.sleep(timer)

        for _, key in self.keyboard.items():
            key.set_released()

    def process(self, strip):
        for _, key in self.keyboard.items():
            if key.state == State.Pressed:
                key.state = State.Hold
                if self.velocity:
                    key.led.set_color(velocity=key.velocity)
                else:
                    key.led.set_color()
            if key.state == State.Released and key.led.color:
                key.led.process(self.sustain_pressed)
        strip.set_color(self.keyboard)
        strip.show()
