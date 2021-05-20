class LED:
    def __init__(self, index, velocity):
        self.index      = index
        self.velocity   = velocity
        self.fading     = False
        self.r          = 0
        self.g          = 0
        self.b          = 255

    def process(self, fade_speed, velocity, color_mode):
        if self.fading:
            self.r = int(self.r * fade_speed) if self.r > 0 else 0
            self.g = int(self.g * fade_speed) if self.g > 0 else 0
            self.b = int(self.b * fade_speed) if self.b > 0 else 0

        if velocity:
            self.r = int(interp(self.velocity, [25, 100], [1,self.r]))
            self.g = int(interp(self.velocity, [25, 100], [1,self.g]))
            self.b = int(interp(self.velocity, [25, 100], [1,self.b]))
        
        self.velocity = self.r + self.g + self.b