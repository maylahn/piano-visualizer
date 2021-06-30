from rpi_ws281x import Adafruit_NeoPixel
from copy import deepcopy
from config import *
from utils.color import Color
from mode import Mode
import time

class Strip:
    def __init__(self):
        self.strip = None
        self.notes = None
        self.modes = []
        self.active_mode = None
        self.config_mode = False
        self.leds = []
        self.config_RGB = None
        self.audio = None

    def setup(self, notes, audio):
        self.notes = notes
        self.audio = audio
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
        self.init_modes()
        self.active_mode = self.modes[LED_STARTUP_MODE]

    def init_modes(self):
        self.modes.append(
            Mode(
                name="monochrome",
                index=1,
                color=Color(0, 0, 255),
                touch_sensitive=False,
                fade_led=True,
                fade_speed=0.95,
            )
        )
        self.modes.append(
            Mode(
                name="multicolor",
                index=2,
                color=Color(255, 255, 0),
                touch_sensitive=False,
                fade_led=True,
                fade_speed=0.95,
            )
        )
        self.modes.append(
            Mode(
                name="rainbow",
                index=3,
                color=Color(255, 0, 255),
                touch_sensitive=False,
                fade_led=True,
                fade_speed=0.95,
            )
        )
        self.modes.append(
            Mode(
                name="mic",
                index=4,
                color=Color(255, 0, 255),
                touch_sensitive=False,
                fade_led=True,
                fade_speed=0.5,
            )
        )

    def startup_sequence(self):
        self.clear()
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color.hex(LED_STARTUP_COLOR).toLED())
            self.show()
        self.clear()

    def clear(self):
        for i in range(self.strip.numPixels()):
            self.strip.setPixelColor(i, Color(0, 0, 0).toLED())

    def toggle_config_mode(self):
        self.config_mode = not self.config_mode
        if self.config_mode:
            self.leds.clear()
            self.clear()
            self.leds = self.active_mode.getConfigSetup(self.notes)
        else:
            self.leds.clear()
            self.clear()

    def next_mode(self):
        for i, mode in enumerate(self.modes):
            if mode == self.active_mode:
                self.active_mode = self.modes[(i + 1) % len(self.modes)]
                self.clear()
                self.leds = self.active_mode.getConfigSetup(self.notes)
                return

    def show(self):
        self.strip.show()

    def process(self, note, velocity, config):
        if note:
            if note.name == PIANO_ACCESS_CONFIG_MODE_NOTE and config:
                self.toggle_config_mode()
                return
            if self.config_mode:
                if note.name == CONFIG_NEXT_MODE and velocity > 0:
                    self.next_mode()
                if note.name == CONFIG_RED:
                    self.config_RGB = CONFIG_RED
                if note.name == CONFIG_GREEN:
                    self.config_RGB = CONFIG_GREEN
                if note.name == CONFIG_BLUE:
                    self.config_RGB = CONFIG_BLUE

                if note.name == CONFIG_PLUS and self.config_RGB:
                    self.active_mode.color.change(self.config_RGB, 10)
                if note.name == CONFIG_MINUS:
                    self.active_mode.color.change(self.config_RGB, -10)
            elif self.active_mode.name == "mic":
                return
            else:
                added_led = self.active_mode.getLED(note, velocity)
                for led in self.leds:
                    if led.index == added_led.index and added_led.velocity == 0:
                        led.is_pressed = False
                        return
                    elif led.index == added_led.index:
                        led.is_pressed = True
                        led.color = deepcopy(self.active_mode.color)
                        return
                self.leds.append(added_led)
        else:
            if self.active_mode.name == "mic":
                frequency = self.audio.get_frequency()
                if frequency:
                    for note in self.notes:
                        if self.notes[note].freq == frequency:
                            self.leds.append(
                                self.active_mode.getLED(self.notes[note], 100)
                            )

            for led in self.leds:
                if self.config_mode:
                    led.process()
                    self.strip.setPixelColor(led.index, led.color.toLED())
                else:
                    if led.color.isOn():
                        led.process()
                        self.strip.setPixelColor(led.index, led.color.toLED())
                    else:
                        self.leds.remove(led)
