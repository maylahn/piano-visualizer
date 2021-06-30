import pyaudio
import struct
import numpy as np
from config import *


class Audio:
    def __init__(self):
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
        self.max = 0

    def find_nearest(self, value):
        array = np.asarray(self.piano_frequencies)
        idx = (np.abs(array - value)).argmin()
        return array[idx]

    def calculate_frequencies(self):
        frequencies = []
        for x, _ in enumerate(PIANO_NOTES, 1):
            frequencies.append(2 ** ((x - 49) / 12) * 440)
        return frequencies

    def get_frequency(self):
        data = self.stream.read(AUDIO_CHUNK_SIZE, exception_on_overflow=False)
        data_in = np.frombuffer(data, dtype=np.int16)
        data_fft = np.fft.rfft(data_in) / ((len(data_in) // 2))
        max_mag = 20 * np.log10(np.max(np.abs(data_fft)))

        if max_mag < AUDIO_DECIBEL_THRESHHOLD:
            return None
        else:
            index = np.argmax(np.abs(data_fft))
            freq = np.fft.fftfreq(AUDIO_CHUNK_SIZE, d=1 / AUDIO_SAMPLE_RATE)
            # print(freq[index])
            return self.find_nearest(freq[index])
