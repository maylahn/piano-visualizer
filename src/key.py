from settings import *
import time


class Key:
    def __init__(self, note, frequency):
        self.note = note
        self.frequency = frequency
        self.led = None
        self.pressed = None
        self.velocity = None

    @staticmethod
    def init_keyboard():
        keyboard = {}
        for index, note in enumerate(PIANO_NOTES, 1):
            keyboard[note] = Key(note, Key.get_frequency(index))
        return keyboard

    @staticmethod
    def get_frequency(index):
        return 440 * 2 ** ((index - 49) / 12)

    @staticmethod
    def index_to_name(key):
        return PIANO_NOTES[key - PIANO_KEY_OFFSET]

    def set_hold(self, velocity=100):
        self.pressed = True
        self.led.fade_hold = True
        self.led.velocity = velocity
        self.led.set_color()

    def set_pressed(self, velocity=100):
        self.pressed = False
        self.led.fade_hold = False
        self.led.velocity = velocity
        self.led.set_color()

    def set_released(self):
        self.pressed = False
        self.led.fade_hold = False
        self.velocity = 0

    def get_led_index(self, index):
        if index < 36:
            index = index * 2 + 1
        elif index > 71:
            index = index * 2 - 1
        else:
            index = index * 2
        return index

    def is_pressed(self):
        return self.pressed

    def __str__(self):
        return "Note: {}".format(self.note)
