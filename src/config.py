import pyaudio

# LED config
LED_COUNT        = 176
LED_PIN          = 18
LED_FREQ_HZ      = 800000
LED_DMA          = 10
LED_BRIGHTNESS   = 255
LED_INVERT       = False
LED_CHANNEL      = 0
LED_STARTUP_MODE = 0

# Piano Settings
PIANO_NOTES = ['A0', 'A#0', 'B0', 'C1', 'C#1', 'D1', 'D#1', 'E1', 'F1', 'F#1', 'G1', 'G#1', 'A1', 'A#1', 'B1', 'C2', 'C#2', 'D2', 'D#2', 'E2', 'F2', 'F#2', 'G2', 'G#2', 'A2', 'A#2', 'B2', 'C3', 'C#3', 'D3', 'D#3', 'E3', 'F3', 'F#3', 'G3', 'G#3', 'A3', 'A#3', 'B3', 'C4', 'C#4', 'D4', 'D#4', 'E4', 'F4', 'F#4', 'G4', 'G#4', 'A4', 'A#4', 'B4', 'C5', 'C#5', 'D5', 'D#5', 'E5', 'F5', 'F#5', 'G5', 'G#5', 'A5', 'A#5', 'B5', 'C6', 'C#6', 'D6', 'D#6', 'E6', 'F6', 'F#6', 'G6', 'G#6', 'A6', 'A#6', 'B6', 'C7', 'C#7', 'D7', 'D#7', 'E7', 'F7', 'F#7', 'G7', 'G#7', 'A7', 'A#7', 'B7', 'C8']
PIANO_MIDI_PORT = 'Digital Piano:Digital Piano MIDI 1'
PIANO_RECONNECT_TIMER = 3
PIANO_KEY_OFFSET = 21
PIANO_ACCESS_SETTINGS_MODE_TIMER = 0.5
PIANO_ACCESS_CONFIG_MODE_NOTE = 'A0'


# Config Mode Settings
CONFIG_MODE_INDEX = ['C#1', 'D#1', 'F#1', 'G#1']
CONFIG_NEXT_MODE = 'A#0'

CONFIG_RED = 'F#2'
CONFIG_GREEN = 'G#2'
CONFIG_BLUE = 'A#2'

CONFIG_PLUS = 'D#3'
CONFIG_MINUS = 'C#3'

CONFIG_COLOR_START = 'C4'

# Audio Settings
AUDIO_FORMAT = pyaudio.paInt16
AUDIO_DEVICE_INDEX = 0
AUDIO_CHANNELS = 1
AUDIO_SAMPLE_RATE = 44100
AUDIO_CHUNK_SIZE = 1024 * 4
AUDIO_DECIBEL_THRESHHOLD = 30

