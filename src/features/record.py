from time import time
from datetime import datetime
from mido import MidiTrack, MidiFile, Message
from pathlib import Path
from settings import (
    MIDI_RECORD_SAVE_DIRECTORY,
    MIDI_RECORD_SAVE_FOLDER_FORMAT,
    MIDI_RECORD_SAVE_TIME_FORMAT,
    MIDI_TEMPO_MULTIPLIER,
)


class RecordHandler:
    def __init__(self):
        self.recording = None
        self.timer_record_midi = None
        self.file = None
        self.track = None
        self.tempo = None

    def start(self):
        self.track = MidiTrack()
        self.file = MidiFile()
        self.file.tracks.append(self.track)
        self.tempo = time()

    def stop(self):
        if self.file:
            del self.track[0]
            del self.track[-1]

            Path(
                "{}/{}".format(
                    MIDI_RECORD_SAVE_DIRECTORY,
                    datetime.now().strftime(MIDI_RECORD_SAVE_FOLDER_FORMAT),
                )
            ).mkdir(parents=True, exist_ok=True)

            filename = "{}/{}/{}.mid".format(
                MIDI_RECORD_SAVE_DIRECTORY,
                datetime.now().strftime(MIDI_RECORD_SAVE_FOLDER_FORMAT),
                datetime.now().strftime(MIDI_RECORD_SAVE_TIME_FORMAT),
            )
            self.file.save(filename=filename)
            self.file = None

    def process(self, msg):
        if msg.type == "note_on":
            type = "note_on" if msg.velocity > 0 else "note_off"
            self.track.append(
                Message(
                    type,
                    note=msg.note,
                    velocity=msg.velocity,
                    time=int((time() - self.tempo) * MIDI_TEMPO_MULTIPLIER),
                )
            )
        if msg.type == "control_change":
            self.track.append(
                Message(
                    "control_change",
                    control=64,
                    value=msg.value,
                    time=int((time() - self.tempo) * MIDI_TEMPO_MULTIPLIER),
                )
            )
        self.tempo = time()
