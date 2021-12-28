from time import sleep
import random


class Sequence:
    def __init__(self, name):
        self.name = name
        self.sequences = [self.static_show, self.ascend_show, self.descend_show]

    def show(self, strip, keyboard):
        strip.clear()
        random.choice(self.sequences)(strip, keyboard)

    def static_show(self, strip, keyboard):
        for key in keyboard.keys:
            key.set_pressed()
            key.led.set_color(velocity=50)

        strip.set_color(keyboard)
        strip.show()

        sleep(1)

        for key in keyboard.keys:
            key.set_released()

    def pulse_show(self, strip, keyboard):
        pass

    def ascend_show(self, strip, keyboard):
        for key in keyboard.keys:
            key.set_pressed()
            key.led.set_color(velocity=50)

            strip.set_color(keyboard)
            strip.show()

        sleep(0.5)

        for key in keyboard.keys:
            key.set_released()

    def descend_show(self, strip, keyboard):
        for key in reversed(keyboard.keys):
            key.set_pressed()
            key.led.set_color(velocity=50)

            strip.set_color(keyboard)
            strip.show()

        sleep(0.5)

        for key in keyboard.keys:
            key.set_released()
