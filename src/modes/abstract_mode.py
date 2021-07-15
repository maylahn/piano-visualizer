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

    @abstractmethod
    def process(self, strip):
        pass

    def show(self, strip, timer=1):
        for _, key in self.keyboard.items():
            key.set_pressed()
            key.led.set_color()
        strip.set_color(self.keyboard)
        strip.show()
        time.sleep(timer)

        for _, key in self.keyboard.items():
            key.set_released()
