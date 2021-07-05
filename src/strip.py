from rpi_ws281x import Adafruit_NeoPixel
from settings import *
from settings_color import STARTUP_COLOR
from color import Color

class Strip:
    def __init__(self):
        self.strip = Adafruit_NeoPixel(
            LED_COUNT,
            LED_PIN,
            LED_FREQ_HZ,
            LED_DMA,
            LED_INVERT,
            LED_BRIGHTNESS,
            LED_CHANNEL,
        )
        self.strip.begin()
        self.startup_sequence()

    def startup_sequence(self):
        self.clear()
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color.hex(STARTUP_COLOR).toLED())
            self.show()
        self.clear()
        self.show()

    def clear(self):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(0, 0, 0).toLED())

    def show(self):
        self.strip.show()

    def setColor(self, key):
        self.strip.setPixelColor(key.led.index, key.led.color.toLED())

    @staticmethod
    def get_led_index(index):
        if index < 36:
            index = index * 2 + 1
        elif index > 71:
            index = index * 2 - 1
        else:
            index = index * 2
        return index