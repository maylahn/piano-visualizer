from numpy import interp
from rainbow import Rainbow
from strip import Strip
from piano import Piano

piano = Piano()
strip = Strip()

while True:
    while piano.is_connected():
        led = piano.get_input()
        if led:
            strip.add_led(led)
        strip.process()
        strip.show()
    else:
        piano.connect()
        if piano.is_connected():
            strip.setup()
            strip.startup_sequence()