from color import Color
from copy import deepcopy
from settings import LED_FADE_SPEED_WITH_SUSTAIN, LED_FADE_SPEED_WITHOUT_SUSTAIN


class LED:
    def __init__(
        self,
        fading=True,
        default_color=Color.name("white"),
    ):
        self.fading = fading
        self.force_control = False
        self.default_color = default_color
        self.color = None

    def set_color(self, color=None, velocity=100):
        if color:
            self.color = color.brightness(velocity)
        else:
            self.color = deepcopy(self.default_color).brightness(velocity)

    def process(self, sustain):
        if not self.force_control:
            if self.fading:
                if sustain:
                    self.color.fade(LED_FADE_SPEED_WITH_SUSTAIN)
                else:
                    self.color.fade(LED_FADE_SPEED_WITHOUT_SUSTAIN)
                if not self.color.isOn():
                    self.color = None
            else:
                if self.color.isOn():
                    self.color.off()
                else:
                    self.color = None

    def __str__(self):
        return "Color: {}".format(self.color)
