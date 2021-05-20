from rpi_ws281x import *

# LED Settings
LED_COUNT      = 176
LED_PIN        = 18
LED_FREQ_HZ    = 800000
LED_DMA        = 10
LED_BRIGHTNESS = 255
LED_INVERT     = False
LED_CHANNEL    = 0

class Strip:
    def __init__(self):
        self.strip = None
        self.fade_speed = 0.95
        self.color_mode = None
        self.active = []
        self.config_mode = False

    def setup(self):
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()

    def startup_sequence(self):
        self.clear()
        for j in range(0, 30, 1):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(j, 0, j))
            self.show()
        for j in range(30, 0, -1):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(j, 0, j))
            self.show()
        self.clear()

    def set_color_mode(self, mode):
        pass

    def config_mode():
        if not self.config_mode:
            self.active.clear()
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(0, 0, 0))
            self.show()
        self.config_mode = not self.config_mode

    def clear(self):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(0,0,0))
        self.show()

    def add_led(self, led):
        for active_led in self.active:
            if active_led.index == led.index and led.velocity == 0:
                active_led.fading = True
                return
            elif active_led.index == led.index:
                active_led.fading = False
                active_led.b = 255
                return
        self.active.append(led)

    def process(self):
        for led in self.active:
            if led.velocity > 0:
                led.process(fade_speed=self.fade_speed, velocity=False, color_mode=None)
                self.strip.setPixelColor(led.index, Color(led.r, led.g, led.b))
            else:
                self.active.remove(led)

    def show(self):
        self.strip.show()