import os
import mido
import time

from config import *

class Piano:
    def __init__(self):
        self.connection = None
        self.timer = None
        self.notes = {}

    def setup(self):
        for i, name in enumerate(PIANO_NOTES):
            self.notes[name] = Note(name, self.calculate_led_index(i), self.calculate_frequency(i))
        
    def calculate_frequency(self, index):
        return 440 * 2** ((index - 48) / 12)

    def calculate_led_index(self, i):
        if (i < 36):
            i = i * 2 + 1
        elif (i > 71):
            i = i * 2 - 1
        else:
            i = i * 2
        return i

    def get_note(self, name):
        return self.notes[name]

    def get_note_name(self, note):
        return PIANO_NOTES[note - PIANO_KEY_OFFSET]

    def reconnect(self):
        if os.path.exists('/dev/midi'):
            self.connection = mido.open_input(PIANO_MIDI_PORT)
            return True
        else:
            self.connection = None
            time.sleep(PIANO_RECONNECT_TIMER)
            return False

    def get_input(self):
        for key in self.connection.iter_pending():
            if key.type=='note_on':
                if self.get_note_name(key.note) == PIANO_ACCESS_CONFIG_MODE_NOTE and key.velocity > 0:
                    self.timer = time.process_time()
                if self.get_note_name(key.note) == PIANO_ACCESS_CONFIG_MODE_NOTE and key.velocity <= 0 and (time.process_time() - self.timer) > PIANO_ACCESS_SETTINGS_MODE_TIMER:
                    return self.get_note(self.get_note_name(key.note)), key.velocity, True
                return self.get_note(self.get_note_name(key.note)), key.velocity, None
        return None, None, None

    def is_connected(self):
        return self.connection and os.path.exists('/dev/midi')

class Note:
    def __init__(self, name, led_index, freq):
        self.name = name
        self.led_index = led_index
        self.freq = freq

