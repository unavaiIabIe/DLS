from Connector import Connector
import pygame
from Variables import screen


class InputConnector(Connector):
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def connect(self, y, output_pos):
        pygame.draw.line(screen, self.wire_color, (self.x + 10, y),
                         (output_pos[0] - 10, output_pos[1]), 5)
