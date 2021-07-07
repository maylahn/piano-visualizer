from abc import ABC, abstractmethod


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
