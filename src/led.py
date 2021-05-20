from utils.color import Color

class LED:
    def __init__(self, index, velocity=100, touch_sensitive=False, fade_led=True, fade_speed=0.9, color_mode=Color(255, 255, 255)):
        self.index           = index
        self.velocity        = velocity
        self.is_pressed      = True
        self.touch_sensitive = touch_sensitive
        self.fade_led        = fade_led
        self.fade_speed      = fade_speed
        self.color           = color_mode

    def process(self):
        if not self.is_pressed:
            if self.fade_led:
                self.color.fade(self.fade_speed)
            else:
                self.color = Color(0, 0, 0)

            if self.touch_sensitive:
                self.color = self.color.velocity(self.velocity)