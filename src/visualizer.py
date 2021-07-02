import sys
from piano import Piano

if __name__ == '__main__':
    args = sys.argv[1:]

    if args:
        if args[0] == '--disable-mic':
            piano = Piano(mic_active=False)
        else:
            print('Unregonized argument. exiting..')
            sys.exit(0)
    else:
        piano = Piano()

    piano.init_led_strip()
    piano.init_keyboard()
    piano.init_color_modes()
    for _, mode in piano.modes.items():
        mode.init_leds()
    piano.init_config_mode()
    if piano.mic_active:
        piano.init_audio()


    while True:
        while piano.is_connected():
            piano.process_input()
        else:
            piano.reconnect()