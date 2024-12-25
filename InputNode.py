from Node import Node
import pygame
from Variables import screen


class InputNode(Node):
    def draw(self, y):
        pygame.draw.circle(screen, self.color, (0, y), 12)
