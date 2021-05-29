from copy import deepcopy

from numpy import not_equal
from config import *
from led import *

class Mode:
    def __init__(self, name, index, color, touch_sensitive, fade_led, fade_speed):
        self.name = name
        self.index = index
        self.leds = []
        self.color = color
        self.touch_sensitive = touch_sensitive
        self.fade_led = fade_led
        self.fade_speed = fade_speed


    def getConfigSetup(self, notes):

        for i in range(self.index):
            self.leds.append(LED(notes[CONFIG_MODE_INDEX[i]].led_index, color=Color(0, 20, 0)))

        for i, note in enumerate(PIANO_NOTES):
            if note == CONFIG_COLOR_START:
                for note in PIANO_NOTES[i:]:
                    self.leds.append(LED(notes[note].led_index, color=self.color))


        self.leds.append(LED(notes[CONFIG_NEXT_MODE].led_index, color=Color(255, 255, 255), pulsing=True))

        self.leds.append(LED(notes[CONFIG_RED].led_index,       color=Color(self.color.red, 0, 0)))
        self.leds.append(LED(notes[CONFIG_GREEN].led_index,     color=Color(0, self.color.green, 0)))
        self.leds.append(LED(notes[CONFIG_BLUE].led_index,      color=Color(0, 0, self.color.blue)))

        self.leds.append(LED(notes[CONFIG_PLUS].led_index,      color=Color(255, 255, 255)))
        self.leds.append(LED(notes[CONFIG_MINUS].led_index,     color=Color(20, 20, 20)))
        
        return self.leds


    def getLED(self, note, velocity):
        return LED(note.led_index, velocity, self.touch_sensitive, self.fade_led, self.fade_speed, deepcopy(self.color))