# Piano Visualizer

Piano visualization with a LED-Strip for a e-piano keyboard running on a Raspberry Pi.

Using [Mido](https://mido.readthedocs.io/en/latest/) to read Midi Signals over USB and [rpi-ws281x](https://github.com/jgarff/rpi_ws281x) library to control the LEDs.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all requirements

```
pip install -r requirements.txt
```

Also following Libraries are required:
```
sudo apt-get install libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
```

## Usage
config.py includes all user specific settings
* piano settings (Midi port, reconnect timer, midi offset etc.)
* led settings (Number of leds, GPIO Pin etc.)
* piano config mode settings
* audio settings for FFT (Microphone index, sample rate etc.)

## Future implementations

### High Priority
* fix first draft of an audio analyizer via the fast fourier transformation to make it usable (The goal is to whistle or sing a melody and the specific LEDs for that frequency light up, so you can easily play it back)
* refactor the whole 'config mode' code.

### Medium Priority
* fix the preset color modes/schemas (monochrome, multicolor, rainbow)
* write a document for all config settings
* write a document how to use the config mode

### Low Priority
* implement a setup routine for other pianos


## Changelog
### 0.3 (2011-06-30)
- format code with black
- add licence
  
### 0.2 (2021-05-29)
- added a 'config mode' accessible via a specific piano key to change color scheme of led
- added first draft of an audio analyzer the fast fourier transformation (eg. you want to learn a melody and whistle that in)

### 0.1 (2021-05-20)
- basic functionality to light up LEDs with keypresses
- added fading effect for keys
- automatically reconnection, when piano is recognized