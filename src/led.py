from color import Color
from copy import deepcopy


class LED:
    def __init__(
        self,
        fade_led=True,
        fade_speed=0.9,
        default_color=Color.name("white"),
    ):
        self.fade_led = fade_led
        self.fade_speed = fade_speed
        self.fade_hold = False
        self.default_color = default_color
        self.color = None

    def set_color(self, color=None, velocity=100):
        if color:
            self.color = color.brightness(velocity)
        else:
            self.color = deepcopy(self.default_color).brightness(velocity)

    def process(self):
        if not self.fade_hold:
            if self.fade_led:
                self.color.fade(self.fade_speed)
                if not self.color.isOn():
                    self.color = None
            else:
                if self.color.isOn():
                    self.color.off()
                else:
                    self.color = None

    def __str__(self):
        return "Color: {}".format(self.color)
