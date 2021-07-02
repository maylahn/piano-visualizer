import os
import mido
import time

from copy import deepcopy
from settings import *
from strip import Strip
from audio import Audio
from color_mode import ColorMode
from config_mode import ConfigMode
from key import Key

class Piano:

    def __init__(self, mic_active=False):
        self.keyboard = None
        self.active_keyboard = {}
        self.mic_active = mic_active
        self.access_settings_timer = None
        self.midi_connection = None
        self.modes = None
        self.config_mode = None
        self.active_mode = None
        self.audio = None
        self.strip = None
        

    def init_led_strip(self):
        self.strip = Strip()

    def init_audio(self):
        self.audio = Audio()

    def init_color_modes(self):
        self.modes = ColorMode.init_color_modes(self.keyboard, self.active_keyboard)
        self.active_mode = self.modes[PIANO_STARTUP_MODE] or self.modes['monochrome']

    def init_config_mode(self):
        self.config_mode = ConfigMode()

    def init_keyboard(self):
        self.keyboard = Key.init_keys()

    def reconnect(self):
        if os.path.exists("/dev/midi"):
            self.midi_connection = mido.open_input(PIANO_MIDI_PORT)
            return True
        else:
            self.midi_connection = None
            time.sleep(PIANO_RECONNECT_TIMER)
            return False

    def is_connected(self):
        return self.midi_connection and os.path.exists("/dev/midi")

    def update_key(self, msg):
        key = self.active_keyboard.get(Key.index_to_name(msg.note))
        if key:
            if msg.velocity == 0:
                key.is_pressed = False
                key.led.fade_hold = False
                key.velocity = msg.velocity
        else:   
            key = deepcopy(self.keyboard[Key.index_to_name(msg.note)])
            key.is_pressed = True
            key.velocity = msg.velocity
            key.led.color = key.led.default_color
            self.active_keyboard[key.name] = key
        return key

    def start_timer(self):
        self.access_settings_timer = time.process_time()

    def stop_timer(self):
        return time.process_time() - self.access_settings_timer

    def process_input(self):
        for msg in self.midi_connection.iter_pending():
            if msg.type == "note_on":
                key = self.update_key(msg)
                if key.name == PIANO_ACCESS_CONFIG_MODE_NOTE and key.is_pressed:
                    self.start_timer()
                if key.name == PIANO_ACCESS_CONFIG_MODE_NOTE and not key.is_pressed:
                    if self.stop_timer() > PIANO_ACCESS_SETTINGS_MODE_TIMER:
                        self.config_mode.toggle()

        if self.config_mode.is_active():
            pass
            #self.config_mode.process(self.strip, note)
        else:
            self.active_mode.process(self.strip)
