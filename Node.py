class Node:
    def __init__(self):
        self.color = (100, 0, 255)
        self.on = 0

    def flip(self):
        if self.on == 0:
            self.color = (255, 0, 100)
            self.on = 1
        else:
            self.color = (100, 0, 255)
            self.on = 0
