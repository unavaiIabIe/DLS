from Node import Node
import pygame
from Variables import screen, width


class OutputNode(Node):
    def draw(self, y):
        pygame.draw.circle(screen, self.color, (width, y), 12)

    def correct_color(self):
        if self.on:
            self.color = (255, 0, 100)

        else:
            self.color = (100, 0, 255)
