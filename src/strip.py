from rpi_ws281x import Adafruit_NeoPixel
from settings import *
from led import LED
from utils.color import Color
from copy import deepcopy

class Strip:
    def __init__(self):
        self.strip = None
        self.touch_sensitive = False
        self.fade_led = True
        self.fade_speed = 0.95
        self.color_mode = Color(255, 0, 255)
        self.leds = []
        self.config_mode = False

    def setup(self):
        self.strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
        self.strip.begin()

    def startup_sequence(self):
        self.clear()
        for j in range(0, 30, 1):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(j, 0, j).toLED())
            self.show()
        for j in range(30, 0, -1):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(j, 0, j).toLED())
            self.show()
        self.clear()

    def set_color_mode(self, color_mode):
        self.color_mode = color_mode

    def config_mode(self):
        if not self.config_mode:
            self.leds.clear()
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(0, 0, 0).toLED())
            self.show()
        self.config_mode = not self.config_mode

    def clear(self):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(0, 0, 0).toLED())
        self.show()

    def add_led(self, key, velocity):
        added_led = LED(key, velocity, self.touch_sensitive, self.fade_led, self.fade_speed, deepcopy(self.color_mode))
        for led in self.leds:
            if led.index == added_led.index and added_led.velocity == 0:
                led.is_pressed = False
                return
            elif led.index == added_led.index:
                led.is_pressed = True
                led.color = deepcopy(self.color_mode)
                return
        self.active.append(led)

    def process(self):
        for led in self.leds:
            if led.color.isOn():
                led.process()
                self.strip.setPixelColor(led.index, led.color.toLED())
            else:
                self.leds.remove(led)

    def show(self):
        self.strip.show()