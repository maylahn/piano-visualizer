import os
from mido import MidiFile
from time import sleep
from glob import glob
from datetime import datetime
from multiprocessing import Process, Queue
from settings import MIDI_RECORD_SAVE_DIRECTORY, MIDI_RECORD_SAVE_FOLDER_FORMAT


class PlaybackHandler:
    def __init__(self):
        self.queue = None
        self.file = None
        self.playback_process = None

    def start(self):
        self.queue = Queue()
        self.playback_process = PlaybackProcess(self.queue, self.file)
        self.playback_process.start()

    def stop(self):
        self.playback_process = None

    def process(self, output_port):
        msg = None
        if not self.queue.empty():
            msg = self.queue.get(block=False)
        if msg:
            output_port.send(msg)
            return msg

    def set_latest_file(self):
        folder_path = "{}/{}".format(
            MIDI_RECORD_SAVE_DIRECTORY,
            datetime.now().strftime(MIDI_RECORD_SAVE_FOLDER_FORMAT),
        )
        file_type = "/*mid"
        files = glob(folder_path + file_type)
        latest_file = max(files, key=os.path.getctime)
        self.file = latest_file


class PlaybackProcess(Process):
    def __init__(self, queue, file):
        super().__init__()
        self.queue = queue
        self.file = file

    def run(self):
        for msg in MidiFile(self.file):
            sleep(msg.time)
            self.queue.put(msg)
