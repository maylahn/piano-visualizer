from numpy import interp
from settings import *
import random


class Color:
    default_colors = {
        "white": "FFFFFF",
        "red": "FF0000",
        "lime": "00FF00",
        "blue": "0000FF",
        "yellow": "FFFF00",
        "cyan": "00FFFF",
        "magenta": "FF00FF",
        "silver": "C0C0C0",
        "gray": "808080",
        "maroon": "800000",
        "olive": "808000",
        "green": "008000",
        "purple": "800080",
        "teal": "008080",
        "navy": "000080",
    }

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
        if name in Color.default_colors:
            return cls.hex(Color.default_colors[name])
        else:
            return cls.hex("FFFFFF")

    @classmethod
    def random(cls):
        return cls.rgb(
            random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
        )

    def fade(
        self,
        fade_speed,
    ):
        self.red = (
            int(self.red * fade_speed)
            if self.red > self.background_red
            else self.background_red
        )
        self.green = (
            int(self.green * fade_speed)
            if self.green > self.background_green
            else self.background_green
        )
        self.blue = (
            int(self.blue * fade_speed)
            if self.blue > self.background_blue
            else self.background_blue
        )

    def brightness(self, velocity):
        self.red = int(interp(velocity, [0, 255], [0, self.red]))
        self.green = int(interp(velocity, [0, 255], [0, self.green]))
        self.blue = int(interp(velocity, [0, 255], [0, self.blue]))
        return self

    def set_background_color(self, default_color, background_light_threshold):
        self.background_red = int(
            interp(background_light_threshold, [0, 255], [0, default_color.red])
        )
        self.background_green = int(
            interp(background_light_threshold, [0, 255], [0, default_color.green])
        )
        self.background_blue = int(
            interp(background_light_threshold, [0, 255], [0, default_color.blue])
        )

    def isOn(self):
        return True if self.red + self.green + self.blue > 0 else False

    def off(self):
        self.red = 0
        self.green = 0
        self.blue = 0

    def toLED(self):
        return self.red << 16 | self.green << 8 | self.blue

    def pulse(self):
        if self.pulsing_direction > 0:
            self.red = (
                self.red + self.pulsing_direction
                if self.red + self.pulsing_direction < 255
                else 255
            )
            if self.red == 255:
                self.pulsing_direction *= -1
        else:
            self.red = (
                self.red + self.pulsing_direction
                if self.red + self.pulsing_direction > 0
                else 0
            )
            if self.red == 0:
                self.pulsing_direction *= -1

    def __str__(self):
        return "R: {}   G: {}   B: {}".format(self.red, self.green, self.blue)
