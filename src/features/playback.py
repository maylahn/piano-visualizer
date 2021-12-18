import os
from mido import MidiFile
from time import sleep
from glob import glob
from datetime import datetime
from multiprocessing import Process
from settings import MIDI_RECORD_SAVE_DIRECTORY, MIDI_RECORD_SAVE_FOLDER_FORMAT


class Playback(Process):
    def __init__(self, queue):
        super().__init__()
        self.playback_queue = queue
        self.file = None

    def run(self):
        for msg in MidiFile(self.file):
            sleep(msg.time)
            if not msg.is_meta:
                self.playback_queue.put(msg)

    def set_latest_file(self):
        folder_path = "{}/{}".format(
            MIDI_RECORD_SAVE_DIRECTORY,
            datetime.now().strftime(MIDI_RECORD_SAVE_FOLDER_FORMAT),
        )
        file_type = "/*mid"
        files = glob(folder_path + file_type)
        latest_file = max(files, key=os.path.getctime)
        self.file = latest_file

