class ConfigMode:

    def __init__(self):
        self.active = False

    def is_active(self):
        return self.active

    def toggle(self):
        self.active = not self.active