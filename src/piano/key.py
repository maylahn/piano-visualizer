from mido import Message
from settings import MIDI_MSG_NOTE_OFFSET
from utility.state import KeyState


class Key:
    def __init__(self, index, note):
        self.index = index
        self.midi_index = index + MIDI_MSG_NOTE_OFFSET
        self.note = note
        self.led_index = self.get_led_index()
        self.frequency = self.get_frequency()
        self.state = KeyState.Released
        self.velocity = 0
        self.led = None

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

    def to_midi_message(self, type):
        return Message(
            "note_{}".format(type),
            note=self.midi_index,
            velocity=127 if type == "on" else 0,
        )

    def __str__(self):
        return "Note: {}  KeyState: {}    Velocity: {}".format(
            self.note, self.state, self.velocity
        )
