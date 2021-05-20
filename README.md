# Piano Visualizer

Piano visualization with a LED-Strip for a Piano. Using [Mido](https://mido.readthedocs.io/en/latest/) to read Midi Signals over USB and [rpi-ws281x](https://github.com/jgarff/rpi_ws281x) library to control the LEDs.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all requirements

```bash
pip install -r requirements.txt
```

## Usage

- configure LED Settings in strip.py
- configure Piano Settings in piano.py

## Changelog

### 0.1 (2021-05-20)
- basic functionality to light up LEDs with keypresses
- added fading effect for keys
- automatically reconnection, when piano is recognized