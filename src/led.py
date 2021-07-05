from color import Color
from copy import deepcopy

class LED:
    def __init__(
        self,
        index,
        velocity=100,
        touch_sensitive=False,
        fade_led=True,
        fade_speed=0.9,
        default_color=Color.name('white'),
        #pulsing=False,
    ):
        self.index = index
        self.velocity = velocity
        self.touch_sensitive = touch_sensitive
        self.fade_led = fade_led
        self.fade_speed = fade_speed
        self.fade_hold = True
        self.default_color = default_color
        self.color = None
        #self.pulsing = pulsing

    def set_color(self):
        if self.touch_sensitive:
            self.color = deepcopy(self.default_color).brightness(self.velocity)
        else:
            self.color = deepcopy(self.default_color)

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

        
        #if self.pulsing:
        #    self.color.pulsing()
        #    return

    def __str__(self):
        return "LED-Index: {}   Velocity: {}   Color: {}".format(self.index, self.velocity, self.color)