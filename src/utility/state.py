import enum


class KeyState(enum.Enum):
    Pressed = 1
    Hold = 2
    Released = 3


class PianoState(enum.Enum):
    Default = 1
    Recording = 2
    Playback = 3
    MicAnalyze = 4
    LED_Off = 5
