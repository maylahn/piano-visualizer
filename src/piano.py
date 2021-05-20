import os
import mido
import time

from settings import *

class Piano:
    def __init__(self):
        self.connection = None
        self.timer = None

    def connect(self):
        if os.path.exists('/dev/midi1'):
            self.connection = mido.open_input(PIANO_MIDI_PORT)
        else:
            time.sleep(PIANO_RECONNECT_TIMER)

    def cleanup(self):
        self.connection = None

    def calc_index(self, note):
        i = note - PIANO_KEY_OFFSET
        if (i < 36):
            i = i * 2 + 1
        elif (i > 71):
            i = i * 2 - 1
        else:
            i = i * 2
        return i

    def get_input(self):
        for key in self.connection.iter_pending():
            if (key.type=='note_on' and self.calc_index(key.note) == 1 and key.velocity > 0):
                self.timer = time.process_time()
            if (key.type=='note_on' and self.calc_index(key.note) == 1 and key.velocity <= 0 and (time.process_time() - self.timer) > PIANO_ACCESS_SETTINGS_MODE_TIMER):
                return -1, None
            if (key.type=='note_on'):
                return self.calc_index(key.note), key.velocity
        return None, None

    def is_connected(self):
        if self.connection and os.path.exists('/dev/midi1'):
            return True
        else:
            self.cleanup()
            return False