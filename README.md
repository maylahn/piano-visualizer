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

### settings.py includes all user specific settings
* piano settings (Midi port, reconnect timer, midi offset etc.)
* led settings (Number of leds, GPIO Pin etc.)
* piano config mode settings
* audio settings for FFT (Microphone index, sample rate etc.)


## Usage
```
python3 visualizer.py <args>
```

|arg|info|
|-|-|
|--disable-mic|disables the initialization of the 'FFT Mode'|



## Current features
* Several 'Color Modes' switchable via a specific configured keyboard note
* 'FFT Mode': Connected microphone gathers information from the enviorement and displays the nearest possible frequency on the led strip. Simply whistle a melody and play it back on your piano.
* Automatic reconnection of the Piano. No need to restart the python app.
* Fully customisable settings for the user in settings.py (Startup Mode, Startup Color, Reconnect Timer, ...)

## Future implementations
* Add Config mode to manually adjust colors / properties of a mode
* write a documentation how to use the config mode
* Add More color modes
* write a documentation for all config settings
* implement a setup routine for other pianos


## Changelog
### 0.5 (2011-07-07)
- refactored modes to use an abstract class for easy creation of new modes
- fixed and added fft mode again 
- add possibility to change modes since the whole config mode doesn't exist anymore


### 0.4 (2011-07-05)
- refactor the whole 'active mode' code.
- now each mode has a own set of all 88 keys and their leds
- Medium Priority: 'fix the preset color modes/schemas (monochrome, multicolor, rainbow)' works now as expected
- implemented config mode doesn't work in this version anymore
- implemented fft mode doesn't work in this version anymore

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