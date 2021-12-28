import pyaudio
import numpy as np
from multiprocessing import Process, Queue
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


class AnalyzerHandler:
    def __init__(self):
        self.queue = None
        self.analyzer_process = None
        self.keyboard = None

    def start(self, keyboard):
        self.queue = Queue()
        self.analyzer_process = AnalyzerProcess(self.queue, keyboard)
        self.analyzer_process.start()

    def stop(self):
        if self.analyzer_process:
            self.analyzer_process.stream.close()
            self.analyzer_process.terminate()
            self.analyzer_process = None

    def process(self):
        msg = None
        if not self.queue.empty():
            msg = self.queue.get(block=False)
        if msg:
            return msg


class AnalyzerProcess(Process):
    def __init__(self, queue, keyboard):
        super().__init__()
        self.queue = queue
        self.keyboard = keyboard
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
        return [key.frequency for key in self.keyboard.keys]

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
                    keys = [
                        key
                        for key in self.keyboard.keys
                        if key.frequency == nearest_freq
                    ]
                    if keys:
                        key_on = keys[0].to_midi_message(type="on")
                        key_off = keys[0].to_midi_message(type="off")
                        self.queue.put(key_on)
                        self.queue.put(key_off)
