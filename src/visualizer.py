from strip import Strip
from piano import Piano

piano = Piano()
strip = Strip()

while True:
    while piano.is_connected():
        key, velocity = piano.get_input()
        if key:
            strip.add_led(key, velocity)
        strip.process()
        strip.show()
    else:
        piano.connect()
        if piano.is_connected():
            strip.setup()
            strip.startup_sequence()