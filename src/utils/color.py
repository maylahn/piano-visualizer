from numpy import interp

class Color:
    def __init__(self, red, green, blue):
        self.red   = red
        self.green = green
        self.blue  = blue

    def fade(self, fade_speed):
        self.red   = int(self.red * fade_speed)   if self.red > 0 else 0
        self.green = int(self.green * fade_speed) if self.green > 0 else 0
        self.blue  = int(self.blue * fade_speed)  if self.blue > 0 else 0

    def velocity(self, velocity):
        self.red   = int(interp(velocity, [25, 100], [1,self.red]))
        self.green = int(interp(velocity, [25, 100], [1,self.green]))
        self.blue  = int(interp(velocity, [25, 100], [1,self.blue]))

    def isOn(self):
        return self.red + self.green + self.blue

    def toLED(self):
        return self.red << 16 | self.green << 8 | self.blue