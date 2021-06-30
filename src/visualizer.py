from strip import Strip
from piano import Piano
from audio import Audio

piano = Piano()
strip = Strip()
audio = Audio()

while True:
    while piano.is_connected():
        key, velocity, config = piano.get_input()
        strip.process(key, velocity, config)
        strip.show()
    else:
        if piano.reconnect():
            piano.setup()
            strip.setup(piano.notes, audio)
            strip.startup_sequence()
