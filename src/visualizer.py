import sys
from piano import Piano

if __name__ == "__main__":
    args = sys.argv[1:]

    if args:
        if args[0] == "--disable-mic":
            piano = Piano(mic_active=False)
        else:
            print("Unregonized argument. exiting..")
            sys.exit(0)
    else:
        piano = Piano()

    while True:
        while piano.is_connected():
            piano.process_input()
        else:
            piano.reconnect()
