class Connector:
    def __init__(self, x, radius, y, chip_connector):
        self.color = (100, 50, 100)
        self.wire_color = (50, 100, 200)
        self.on = 0
        self.x = x
        self.y = y
        self.radius = radius
        if chip_connector:
            self.color = (100, 0, 255)

    def check_wire(self):
        if self.on == 1:
            self.wire_color = (200, 100, 50)
        else:
            self.wire_color = (50, 100, 200)

    def correct_color(self):
        if self.on:
            self.color = (255, 0, 100)

        else:
            self.color = (100, 0, 255)
