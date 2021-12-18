import os
import mido
import os.path
import time
from settings import (
    MIDI_SERVER_HOSTNAME,
    MIDI_SERVER_PORT,
    MIDI_OUTPUT_PORT,
    MIDI_INPUT_PORT,
    MIDI_INPUT_RECONNECT_TIMER,
)


class Midi:
    def __init__(self):
        # Connection
        self.input_port = None
        self.output_port = None

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
