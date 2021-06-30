from numpy import interp
from config import *
import random

class Color:
    def __init__(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue
        self.pulsing_direction = 5

    @classmethod
    def rgb(cls, r, g, b):
        return cls(r, g, b)

    @classmethod
    def hex(cls, hex_color):
        r = int(hex_color[0:2], 16)
        g = int(hex_color[2:4], 16)
        b = int(hex_color[4:6], 16)
        return cls(r, g, b)

    @classmethod
    def name(cls, name):
        if name in LED_DEFAULT_COLORS:
            return cls.hex(LED_DEFAULT_COLORS[name])
        else:
            return cls.hex('FFFFFF')

    @classmethod
    def random(cls):
        return cls.hex(random.choice(list(LED_DEFAULT_COLORS.values())))

    @classmethod
    def rainbow(cls):
        return cls.hex(random.choice(list(LED_DEFAULT_COLORS.values())))

    def fade(self, fade_speed):
        self.red = int(self.red * fade_speed) if self.red > 0 else 0
        self.green = int(self.green * fade_speed) if self.green > 0 else 0
        self.blue = int(self.blue * fade_speed) if self.blue > 0 else 0

    def velocity(self, velocity):
        self.red = int(interp(velocity, [25, 100], [1, self.red]))
        self.green = int(interp(velocity, [25, 100], [1, self.green]))
        self.blue = int(interp(velocity, [25, 100], [1, self.blue]))

    def isOn(self):
        return self.red + self.green + self.blue

    def toLED(self):
        return self.red << 16 | self.green << 8 | self.blue

    def change(self, rgb, value):
        if value > 0:
            if rgb == CONFIG_RED:
                self.red = self.red + value if self.red + value < 255 else 255
            if rgb == CONFIG_GREEN:
                self.green = self.green + value if self.green + value < 255 else 255
            if rgb == CONFIG_BLUE:
                self.blue = self.blue + value if self.blue + value < 255 else 255
        if value < 0:
            if rgb == CONFIG_RED:
                self.red = self.red + value if self.red + value > 0 else 0
            if rgb == CONFIG_GREEN:
                self.green = self.green + value if self.green + value > 0 else 0
            if rgb == CONFIG_BLUE:
                self.blue = self.blue + value if self.blue + value > 0 else 0

    def pulsing(self):
        if self.pulsing_direction > 0:
            self.red = (
                self.red + self.pulsing_direction
                if self.red + self.pulsing_direction < 255
                else 255
            )
            self.green = (
                self.green + self.pulsing_direction
                if self.green + self.pulsing_direction < 255
                else 255
            )
            self.blue = (
                self.blue + self.pulsing_direction
                if self.blue + self.pulsing_direction < 255
                else 255
            )
            if self.red == 255 and self.green == 255 and self.blue == 255:
                self.pulsing_direction *= -1
        if self.pulsing_direction < 0:
            self.red = (
                self.red + self.pulsing_direction
                if self.red + self.pulsing_direction > 0
                else 0
            )
            self.green = (
                self.green + self.pulsing_direction
                if self.green + self.pulsing_direction > 0
                else 0
            )
            self.blue = (
                self.blue + self.pulsing_direction
                if self.blue + self.pulsing_direction > 0
                else 0
            )
            if self.red == 0 and self.green == 0 and self.blue == 0:
                self.pulsing_direction *= -1

    def __str__(self):
        return "R: {}   G: {}   B: {}".format(self.red, self.green, self.blue)
