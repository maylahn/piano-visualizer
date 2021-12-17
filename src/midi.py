import os
import mido
import time
import datetime
from pathlib import Path
from settings import (
    MIDI_RECORD_SAVE_DIRECTORY,
    MIDI_RECORD_SAVE_FOLDER_FORMAT,
    MIDI_RECORD_SAVE_TIME_FORMAT,
    MIDI_SERVER_HOSTNAME,
    MIDI_SERVER_PORT,
    MIDI_OUTPUT_PORT,
    MIDI_INPUT_PORT,
    MIDI_INPUT_RECONNECT_TIMER,
    MIDI_TEMPO_MULTIPLIER,
)


class Midi:
    def __init__(self):
        # Connection
        self.input_port = None
        self.output_port = None

        # Recording
        self.recording = None
        self.timer_record_midi = None
        self.file = None
        self.track = None
        self.tempo = None

        # Server
        self.server = None
        self.hostname = MIDI_SERVER_HOSTNAME
        self.port = MIDI_SERVER_PORT
        self.clients = []

    """
    PIANO CONNECTION
    """

    def port_reconnect(self):
        if os.path.exists("/dev/midi"):
            self.input_port = mido.open_input(MIDI_INPUT_PORT)
            self.output_port = mido.open_output(MIDI_OUTPUT_PORT)
            return True
        else:
            self.input_port = None
            self.output_port = None
            time.sleep(MIDI_INPUT_RECONNECT_TIMER)
            return False

    def port_is_connected(self):
        return self.input_port and os.path.exists("/dev/midi")

    """
    SERVER
    """

    def open_server(self):
        self.server = mido.sockets.PortServer(self.hostname, self.port)

    def check_connection(self):
        client = self.server.accept(block=False)
        if client:
            print("Connection from {}".format(client.name))
            self.clients.append(client)

        for i, client in reversed(list(enumerate(self.clients))):
            if client.closed:
                print("{} disconnected".format(client.name))
                del self.clients[i]

    def send(self, msg):
        for client in self.clients:
            try:
                client.send(msg)
            except:
                pass

    """
    RECORDING
    """
    def start_recording(self):
        self.midi_track = mido.MidiTrack()
        self.midi_file = mido.MidiFile()
        self.midi_file.tracks.append(self.midi_track)
        self.midi_tempo = time.time()


    def stop_recording(self):
        del self.midi_track[0]
        del self.midi_track[-1]

        Path('{}/{}'.format(
            MIDI_RECORD_SAVE_DIRECTORY,
            datetime.datetime.now().strftime(MIDI_RECORD_SAVE_FOLDER_FORMAT)
        )).mkdir(parents=True, exist_ok=True)
        
        filename = "{}/{}/{}.mid".format(
            MIDI_RECORD_SAVE_DIRECTORY,
            datetime.datetime.now().strftime(MIDI_RECORD_SAVE_FOLDER_FORMAT),
            datetime.datetime.now().strftime(MIDI_RECORD_SAVE_TIME_FORMAT),
        )
        self.midi_file.save(filename=filename)

    def add_to_file(self, msg):
        if msg.type == 'note_on':
            type = 'note_on' if msg.velocity > 0 else 'note_off'
            self.midi_track.append(
                mido.Message(
                    type,
                    note=msg.note,
                    velocity=msg.velocity,
                    time=int((time.time() - self.midi_tempo) * MIDI_TEMPO_MULTIPLIER),
                )
            )
        if msg.type == 'control_change':
            self.midi_track.append(
                mido.Message(
                    "control_change",
                    control=64,
                    value=msg.value,
                    time=int((time.time() - self.midi_tempo) * MIDI_TEMPO_MULTIPLIER),
                )
            )
        self.midi_tempo = time.time()


    """
    PLAYBACK
    """
    def playback(self):
        for msg in mido.MidiFile("src/test.mid").play():
            self.output_port.send(msg)
            if self.midi_connection:
                self.midi_connection.send(msg)
