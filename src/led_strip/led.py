from .color import Color
from copy import deepcopy
from settings import (
    LED_BACKGROUND_LIGHT_THRESHOLD,
    LED_FADE_SPEED_WITH_SUSTAIN,
    LED_FADE_SPEED_WITHOUT_SUSTAIN,
)


class LED:
    def __init__(
        self,
        fading=True,
        default_color=Color.name("white"),
        background_light_threshold=LED_BACKGROUND_LIGHT_THRESHOLD,
    ):
        self.fading = fading
        self.force_control = False
        self.default_color = default_color
        self.background_light_threshold = background_light_threshold
        self.color = None

    def set_color(self, color=None, velocity=100):
        if color:
            self.color = color.brightness(velocity)
        else:
            self.color = deepcopy(self.default_color).brightness(velocity)
            self.color.set_background_color(
                self.default_color, self.background_light_threshold
            )

    def process(self, sustain_pressed):
        if not self.force_control:
            if self.fading:
                if sustain_pressed:
                    self.color.fade(LED_FADE_SPEED_WITH_SUSTAIN)
                else:
                    self.color.fade(LED_FADE_SPEED_WITHOUT_SUSTAIN)
            else:
                self.color.off()

    def process_forced(self):
        if not self.color:
            self.color = deepcopy(self.default_color).brightness(255)
        self.color.red = int(self.color.red * 0.99)
        self.color.green = int(self.color.green * 0.99)
        self.color.blue = int(self.color.blue * 0.99)

        if not self.color.isOn():
            self.color = deepcopy(self.default_color).brightness(255)

    def __str__(self):
        return "Color: {}".format(self.color)
