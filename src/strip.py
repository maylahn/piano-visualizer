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
        for j in range(0, 40, 1):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(j, 0, j).toLED())
            self.show()
        for j in range(40, 0, -1):
            for i in range(self.strip.numPixels()):
                self.strip.setPixelColor(i, Color(j, 0, j).toLED())
            self.show()
        self.clear()

    def set_color_mode(self, color_mode):
        self.color_mode = color_mode

    def setup_config_mode(self):
        self.clear()
        self.leds.clear()

        # TODO: make this nice
        red     = LED(19, color_mode=Color(255, 0, 0))
        green   = LED(23, color_mode=Color(0, 255, 0))
        blue    = LED(27, color_mode=Color(0, 0, 255))

        minus   = LED(33, color_mode=Color(30, 30, 30))
        plus    = LED(37, color_mode=Color(255, 255, 255))
        current = LED(78, color_mode=self.color_mode)

        self.leds.append(red)
        self.leds.append(green)
        self.leds.append(blue)
        self.leds.append(minus)
        self.leds.append(plus)
        self.leds.append(current)

    def clear(self):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(0, 0, 0).toLED())
        self.show()

    def add_led(self, key, velocity):
        if key == -1:
            self.config_mode = not self.config_mode
            if self.config_mode:
                self.setup_config_mode()
        if self.config_mode:
            return

        added_led = LED(key, velocity, self.touch_sensitive, self.fade_led, self.fade_speed, deepcopy(self.color_mode))
        for led in self.leds:
            if led.index == added_led.index and added_led.velocity == 0:
                led.is_pressed = False
                return
            elif led.index == added_led.index:
                led.is_pressed = True
                led.color = deepcopy(self.color_mode)
                return
        self.leds.append(added_led)

    def process(self):
        if self.config_mode:
            for led in self.leds:
                led.process()
                self.strip.setPixelColor(led.index, led.color.toLED())
            return

        for led in self.leds:
            if led.color.isOn():
                led.process()
                self.strip.setPixelColor(led.index, led.color.toLED())
            else:
                self.leds.remove(led)

    def show(self):
        self.strip.show()