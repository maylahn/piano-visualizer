from settings import MIDI_MSG_NOTE_OFFSET, PIANO_NOTES
from state import KeyState


class Key:
    def __init__(self, index, note):
        self.index = index
        self.note = note
        self.led_index = self.get_led_index()
        self.frequency = self.get_frequency()
        self.state = KeyState.Released
        self.velocity = 0
        self.led = None

    @staticmethod
    def init_keyboard():
        keyboard = {}
        for index, note in enumerate(PIANO_NOTES, 0):
            keyboard[note] = Key(index, note)
        return keyboard

    @staticmethod
    def index_to_name(key):
        return PIANO_NOTES[key - MIDI_MSG_NOTE_OFFSET]

    def get_frequency(self):
        return 440 * 2 ** ((self.index - 48) / 12)

    def get_led_index(self):
        if self.index < 36:
            return self.index * 2 + 1
        elif self.index > 71:
            return self.index * 2 - 1
        else:
            return self.index * 2

    def set_pressed(self, velocity=100):
        self.state = KeyState.Pressed
        self.velocity = velocity

    def set_released(self, velocity=0):
        self.state = KeyState.Released
        self.velocity = velocity

    def __str__(self):
        return "Note: {}  KeyState: {}    Velocity: {}".format(
            self.note, self.state, self.velocity
        )
