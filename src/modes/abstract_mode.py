from abc import ABC, abstractmethod
import time


class Mode(ABC):
    @abstractmethod
    def __init__(self, name, keyboard):
        self.name = name
        self.keyboard = keyboard

    @abstractmethod
    def init_leds(self):
        pass

    def show(self, strip, timer=1):
        for _, key in self.keyboard.items():
            key.set_hold()
            strip.set_pixel_color(key.led)

        strip.show()
        time.sleep(timer)

        for _, key in self.keyboard.items():
            key.set_released()

    @abstractmethod
    def process(self, strip):
        pass
