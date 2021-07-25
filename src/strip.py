from rpi_ws281x import Adafruit_NeoPixel
from settings import (
    LED_COUNT,
    LED_PIN,
    LED_FREQ_HZ,
    LED_DMA,
    LED_INVERT,
    LED_BRIGHTNESS,
    LED_CHANNEL,
    LED_STARTUP_COLOR,
)
from color import Color
from key import Key


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

    def startup_sequence(self):
        self.clear()
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color.hex(LED_STARTUP_COLOR).toLED())
            self.show()
        self.clear()
        self.show()

    def clear(self):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color.rgb(0, 0, 0).toLED())

    def show(self):
        self.strip.show()

    def set_color(self, obj):
        if type(obj) == Key:
            self.strip.setPixelColor(obj.led_index, obj.led.color.toLED())
        else:
            for _, key in obj.items():
                if key.led.color:
                    self.strip.setPixelColor(key.led_index, key.led.color.toLED())
