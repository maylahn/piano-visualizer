import sys
import mido
import argparse
import pyaudio

from piano.piano import Piano

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Piano LED Visualizer with an LED Strip"
    )

    parser.add_argument("run", help="runs the visualization")
    parser.add_argument(
        "--show-midi", help="display all midi input names", action="store_true"
    )
    parser.add_argument(
        "--show-audio", help="display all audio devices", action="store_true"
    )
    parser.add_argument(
        "--disable-fft",
        help='disables the initialization of the "FFT Mode"',
        action="store_true",
    )

    args = parser.parse_args()

    if args.show_midi:
        print(mido.get_input_names())
        sys.exit()
    if args.show_audio:
        p = pyaudio.PyAudio()
        for i in range(p.get_device_count()):
            print(p.get_device_info_by_index(i))
        sys.exit()
    if args.disable_fft:
        piano = Piano(fft_mode=False)
    else:
        piano = Piano()

    while True:
        while piano.midi.port_is_connected():
            piano.process_input()
        else:
            piano.midi.port_reconnect()
