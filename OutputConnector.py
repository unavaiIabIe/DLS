from Connector import Connector
import pygame
from Variables import screen


class OutputConnector(Connector):
    def draw(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)
