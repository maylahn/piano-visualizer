from multiprocessing import Queue
from settings import *
from led import *
from copy import deepcopy
from .abstract_mode import Mode
from state import State
from audio import Audio


class FFT(Mode):
    def __init__(self, keyboard):
        super().__init__("fft", deepcopy(keyboard))
        self.color_scheme = Color.name("red")
        self.fading = True
        self.queue = Queue()
        self.audio = None
        self.init_leds()

    def init_leds(self):
        for _, key in self.keyboard.items():
            key.led = LED(
                fading=self.fading,
                default_color=self.color_scheme,
            )

    def start_audio(self):
        self.audio = Audio(self.queue)
        self.audio.start()

    def stop_audio(self):
        self.audio.stream.close()
        self.audio.terminate()

    def process(self, strip):
        freq = 0
        if not self.audio:
            self.start_audio()

        if not self.queue.empty():
            freq = self.queue.get(block=False)

        for _, key in self.keyboard.items():
            if key.frequency == freq:
                key.state = State.Pressed
                key.led.set_color()
                key.state = State.Released
            elif key.state == State.Released and key.led.color:
                key.led.process(self.sustain)
        strip.set_color(self.keyboard)
        strip.show()
