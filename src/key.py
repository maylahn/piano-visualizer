from settings import *

class Key:
    def __init__(self, name, frequency):
        self.name = name
        self.freqeuncy = frequency
        self.led = None
        self.pressed = False
        self.velocity = 0

    @staticmethod
    def init_keys():
        keyboard = {}
        for index, name in enumerate(PIANO_NOTES, 1):
            keyboard[name] = Key(
                name, Key.get_frequency(index)
            )
        return keyboard

    @staticmethod
    def get_frequency(index):
        return 440 * 2 ** ((index - 48) / 12)

    @staticmethod
    def index_to_name(key):
        return PIANO_NOTES[key - PIANO_KEY_OFFSET]

    def get_led_index(index):
        if index < 36:
            index = index * 2 + 1
        elif index > 71:
            index = index * 2 - 1
        else:
            index = index * 2
        return index

    def __str__(self):
        return "Name: {}, Pressed: {}, Velocity: {}".format(self.name, self.pressed, self.velocity)
