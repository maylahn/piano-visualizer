import pyaudio

# LED
LED_COUNT = 176
LED_PIN = 18
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False
LED_CHANNEL = 0
LED_FADE_SPEED_WITH_SUSTAIN = 0.95  # 0..1   Higher -> Slower
LED_FADE_SPEED_WITHOUT_SUSTAIN = 0.6  # 0..1   Higher -> Slower
LED_BACKGROUND_LIGHT_THRESHOLD = 0

# Piano
PIANO_NOTES = [
    "A0",
    "A#0",
    "B0",
    "C1",
    "C#1",
    "D1",
    "D#1",
    "E1",
    "F1",
    "F#1",
    "G1",
    "G#1",
    "A1",
    "A#1",
    "B1",
    "C2",
    "C#2",
    "D2",
    "D#2",
    "E2",
    "F2",
    "F#2",
    "G2",
    "G#2",
    "A2",
    "A#2",
    "B2",
    "C3",
    "C#3",
    "D3",
    "D#3",
    "E3",
    "F3",
    "F#3",
    "G3",
    "G#3",
    "A3",
    "A#3",
    "B3",
    "C4",
    "C#4",
    "D4",
    "D#4",
    "E4",
    "F4",
    "F#4",
    "G4",
    "G#4",
    "A4",
    "A#4",
    "B4",
    "C5",
    "C#5",
    "D5",
    "D#5",
    "E5",
    "F5",
    "F#5",
    "G5",
    "G#5",
    "A5",
    "A#5",
    "B5",
    "C6",
    "C#6",
    "D6",
    "D#6",
    "E6",
    "F6",
    "F#6",
    "G6",
    "G#6",
    "A6",
    "A#6",
    "B6",
    "C7",
    "C#7",
    "D7",
    "D#7",
    "E7",
    "F7",
    "F#7",
    "G7",
    "G#7",
    "A7",
    "A#7",
    "B7",
    "C8",
]

PIANO_STARTUP_MODE = "cmajor"

# Function notes + timer threshold
FUNC_TIMER_THRESHOLD = 0.5
FUNCTIONS = [
    {
        "name": "Switch to next mode",
        "note": "A0",
        "indicator": {"note": None, "color": None, "type": None},
    },
    {
        "name": "Start/Stop Midi Recording",
        "note": "C8",
        "indicator": {"note": "C8", "color": "red", "type": "pulse"},
    },
    {
        "name": "Toggle Playback On/Off",
        "note": "B7",
        "indicator": {"note": "B7", "color": "green", "type": "pulse"},
    },
    {
        "name": "Toggle Mic-Analyzer On/Off",
        "note": "A7",
        "indicator": {"note": "A7", "color": "blue", "type": "pulse"},
    },
    {
        "name": "Toggle LEDs On/Off",
        "note": "G7",
        "indicator": {"note": None, "color": None, "type": None},
    },
    {
        "name": "Set Background Light",
        "note": "F7",
        "indicator": {"note": None, "color": None, "type": None},
    },
]

# Midi
MIDI_INPUT_PORT = "Digital Piano:Digital Piano MIDI 1"
MIDI_OUTPUT_PORT = "Digital Piano:Digital Piano MIDI 1"
MIDI_INPUT_RECONNECT_TIMER = 1
MIDI_MSG_NOTE_OFFSET = 21
MIDI_TEMPO_MULTIPLIER = 960

# Midi over TCP/IP
MIDI_SERVER_HOSTNAME = ""
MIDI_SERVER_PORT = 4040

# Midi Recording
MIDI_RECORD_SAVE_DIRECTORY = "recordings"
MIDI_RECORD_SAVE_FOLDER_FORMAT = "%B"
MIDI_RECORD_SAVE_TIME_FORMAT = "%Y-%m-%d_%H-%M-%S"

# Audio
AUDIO_FORMAT = pyaudio.paInt16
AUDIO_DEVICE_INDEX = 0
AUDIO_CHANNELS = 1
AUDIO_SAMPLE_RATE = 44100
AUDIO_CHUNK_SIZE = 1024 * 4
AUDIO_DECIBEL_THRESHOLD = 30
AUDIO_FREQ_MIN = 50
