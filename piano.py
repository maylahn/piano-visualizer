import os
import mido
import time

from led import LED

class Piano:
    def __init__(self):
        self.connection = None
        self.key_offset = 21
        self.reconnect_timeout = 3
        self.settings_timer = None

    def connect(self):
        if os.path.exists('/dev/midi1'):
            self.connection = mido.open_input('Digital Piano:Digital Piano MIDI 1')
        else:
            time.sleep(self.reconnect_timeout)

    def cleanup(self):
        self.connection = None

    def calc_index(self, note):
        i = note - self.key_offset
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
                self.settings_timer = time.process_time()
            if (key.type=='note_on' and self.calc_index(key.note) == 1 and key.velocity <= 0 and (time.process_time() - self.settings_timer) > 1):
                print('SETTINGS MODE')
            if (key.type=='note_on'):
                return LED(self.calc_index(key.note), key.velocity)

    def is_connected(self):
        if self.connection and os.path.exists('/dev/midi1'):
            return True
        else:
            self.cleanup()
            return False