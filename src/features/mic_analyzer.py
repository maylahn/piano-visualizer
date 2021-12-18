import pyaudio
import numpy as np
from multiprocessing import Queue
from settings import (
    AUDIO_FORMAT,
    AUDIO_SAMPLE_RATE,
    AUDIO_CHANNELS,
    AUDIO_DEVICE_INDEX,
    AUDIO_CHUNK_SIZE,
    PIANO_NOTES,
    AUDIO_DECIBEL_THRESHOLD,
    AUDIO_FREQ_MIN,
)
from utility.state import KeyState
from multiprocessing import Process


class Analyzer:
    def __init__(self):
        self.queue = None
        self.audio = None
        self.keyboard = None

    def start(self, keyboard):
        self.queue = Queue()
        self.audio = Audio(self.queue)
        self.keyboard = keyboard
        self.audio.start()

    def stop(self):
        if self.audio:
            self.audio.stream.close()
            self.audio.terminate()
            self.audio = None

    def process(self, strip):
        freq = 0

        if not self.queue.empty():
            freq = self.queue.get(block=False)

        for key in self.keyboard.keys:
            if key.frequency == freq:
                key.state = KeyState.Pressed
                key.led.set_color()
                key.state = KeyState.Released
            elif key.state == KeyState.Released and key.led.color:
                key.led.process(sustain_pressed=True)
        strip.set_color(self.keyboard)
        strip.show()


class Audio(Process):
    def __init__(self, queue):
        super().__init__()
        self.queue = queue
        self.piano_frequencies = self.calculate_frequencies()
        self.audio = pyaudio.PyAudio()
        self.stream = self.audio.open(
            format=AUDIO_FORMAT,
            rate=AUDIO_SAMPLE_RATE,
            channels=AUDIO_CHANNELS,
            input_device_index=AUDIO_DEVICE_INDEX,
            input=True,
            frames_per_buffer=AUDIO_CHUNK_SIZE,
        )
        self.stream.start_stream()

    def find_nearest(self, value):
        array = np.asarray(self.piano_frequencies)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

    def calculate_frequencies(self):
        frequencies = []
        for x, _ in enumerate(PIANO_NOTES, 1):
            frequencies.append(2 ** ((x - 49) / 12) * 440)
        return frequencies

    def run(self):
        while True:
            data = self.stream.read(AUDIO_CHUNK_SIZE, exception_on_overflow=False)
            data_in = np.frombuffer(data, dtype=np.int16)
            data_fft = np.fft.rfft(data_in) / ((len(data_in) // 2))
            max_mag = 20 * np.log10(np.max(np.abs(data_fft)))
            if max_mag < AUDIO_DECIBEL_THRESHOLD:
                continue
            else:
                index = np.argmax(np.abs(data_fft))
                freq = np.fft.fftfreq(AUDIO_CHUNK_SIZE, d=1 / AUDIO_SAMPLE_RATE)
                nearest_freq = self.find_nearest(freq[index])
                if nearest_freq > AUDIO_FREQ_MIN:
                    self.queue.put(nearest_freq)
