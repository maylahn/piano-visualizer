from piano.key import Key
from settings import MIDI_MSG_NOTE_OFFSET, PIANO_NOTES

class Keyboard:
    def __init__(self):
        self.keys = []
        for index, note in enumerate(PIANO_NOTES, 0):
            self.keys.append(Key(index, note))

    def get_key_from_msg(self, msg):
        return self.keys[self.get_key_index_from_msg(msg)]

    def get_force_controlled_keys(self):
        return [x for x in self.keys if x.led.force_control]

    @staticmethod
    def get_key_name_from_msg(msg):
        return PIANO_NOTES[msg.note - MIDI_MSG_NOTE_OFFSET]

    @staticmethod
    def get_key_index_from_msg(msg):
        return msg.note - MIDI_MSG_NOTE_OFFSET

