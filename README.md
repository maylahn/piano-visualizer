# Piano Visualizer

Realtime piano visualization with a LED-Strip for an E-Piano running on a Raspberry Pi.

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
```
python3 visualizer.py <args>
```

|arg|info|
|-|-|
|--disable-fft|disables the initialization of the 'FFT Mode'|
|--show-midi|displays the midi input connected via USB (eg. 'Digital Piano:Digital Piano MIDI 1 16:0') which needs to be set in the settings.py|
|--show-audio|displays all audio devices, where the microphone 'index' needs to be set in the settings.py|




## Features
### Overview

* Several 'Color Schemes' switchable via a specific configured keyboard note
  * Monochrome
  * Dual Color
  * Triple Color
  * Multicolor
  * C-Major Split
  * Rainbow
* Different Sequences for startup / switching to any color scheme
* 'Microphone Analyzer Mode': Connected microphone gathers information from the enviroment and displays the nearest possible matching frequency on the led strip. Simply whistle, hum, sing a melody and see to which note to play on the piano.
* Automatic reconnection of the Piano. No need to restart the python app.
* Customizable settings for a user in settings.py (See below)
* Custom function assigment to keys with led indicator for different modes. Currently includes:
  * Switch to next color scheme
  * Start / Stop midi recording
  * Playback function for recoreded midi files
  * Start / Stop FFT Analyzer 
  * Toggle LEDs On / Off via key
  

### Fully customizable settings in settings.py file
#### Piano settings
* Startup mode
* Function assigment for specific keys which includes
  * Name
  * Note name to poll for
  * Indication of LED if state is active
* Adjustable timer threshold to call given function (eg. hold note 'A3' for 2.5 seconds to switch to next color scheme)


#### Midi settings
* Input / Output Port
* Reconnect Timer
* Midi over TCP/IP 
  * Hostname
  * Port
* Recording
  * Save directory
  * Save format

#### LED settings
* Num of LEDs
* GPIO data pin
* Frequency
* Brightness
* Channel
* Fading speed of LEDs with / without pedal sustain
* Background Light threshold

#### Audio Settings
* Used only for FFT Analyzer if a Microphone is connected
  * Microphone Index
  * Sample Rate
  * Chunk Size
  * Decibel Treshold to light up LED
  * Minimal Frequency to light up LED


## Future implementations
* Make usage of not used LEDs for color modes
* Add more complex color modes (eg. Explosion, Ping Pong, etc.)
* Add possibilty to choose playback of last 5? recorded midi files
  * Or somehow scrolling through all available files
* Automatic startup of http-server of recoreded files to easily transfer them
* implement a setup routine for other pianos


## Changelog
### 0.6 (2021-12-29)
- Add more information to each function in settings file
- Let FFT Analyzer create midi Messages instead of handling the LED strip colors by itself
- Split Playback in two seperate classes (Handler and pure process)
- Add Sequence class for each color scheme
- Move pulse function for forced keys to led class instead of color class
- Add function to use the LEDs as background light
- Cleanup initialisation of Piano class

### 0.5 (2021-07-07)
- refactored modes to use an abstract class for easy creation of new modes
- fixed and added fft mode again 
- add possibility to change modes since the whole config mode doesn't exist anymore


### 0.4 (2021-07-05)
- refactor the whole 'active mode' code.
- now each mode has a own set of all 88 keys and their leds
- Medium Priority: 'fix the preset color modes/schemas (monochrome, multicolor, rainbow)' works now as expected
- implemented config mode doesn't work in this version anymore
- implemented fft mode doesn't work in this version anymore

### 0.3 (2021-06-30)
- format code with black
- add licence
  
### 0.2 (2021-05-29)
- added a 'config mode' accessible via a specific piano key to change color scheme of led
- added first draft of an audio analyzer the fast fourier transformation (eg. you want to learn a melody and whistle that in)

### 0.1 (2021-05-20)
- basic functionality to light up LEDs with keypresses
- added fading effect for keys
- automatically reconnection, when piano is recognized