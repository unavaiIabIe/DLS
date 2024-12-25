import pygame
from InputConnector import InputConnector
from OutputConnector import OutputConnector
from Variables import screen, font


class Chip:
    def __init__(self, op, num_input_connectors, num_output_connectors, x, y):
        self.op = op
        self.num_input = num_input_connectors
        self.num_output = num_output_connectors
        self.input_connectors = []
        self.output_connectors = []
        self.input_connector_positions = []
        self.output_connector_positions = []
        self.x = x
        self.y = y
        for i in range(self.num_input):
            self.input_connectors.append(InputConnector(self.x + 60, 5, self.y + i * 15, True))
            self.input_connector_positions.append([self.x + 60, self.y + i * 15])

        for i in range(self.num_output):
            self.output_connectors.append(OutputConnector(self.x - 10, 5, self.y + i * 15, True))
            self.output_connector_positions.append([self.x - 10, self.y + i * 15])

    def draw(self):
        pygame.draw.rect(screen, (150, 100, 150), (self.x, self.y, 50, 20))
        txt = font.render(self.op, True, (255, 255, 255))
        screen.blit(txt, (self.x, self.y))

        for input_con in self.input_connectors:
            input_con.draw()

        for output_con in self.output_connectors:
            output_con.draw()

    def check_for_connection(self, mouse_pos):
        for i in range(self.num_output):
            if abs(mouse_pos[1] - self.output_connector_positions[i][1]) <= 10 and \
                    (self.output_connector_positions[i][0] - 10 < mouse_pos[0] <
                     self.output_connector_positions[i][0] + 10):
                return [self.output_connectors[i], True, True]

        for i in range(self.num_input):
            if abs(mouse_pos[1] - self.output_connector_positions[i][1]) <= 10 and \
                    (self.input_connector_positions[i][0] - 10 < mouse_pos[0] <
                     self.input_connector_positions[i][0] + 10):
                return [self.input_connectors[i], True, False]

        return [0, False, False]

    def correct_output(self):
        if self.op == "OR":
            self.input_connectors[0].on = self.output_connectors[0].on == 1 or self.output_connectors[1].on == 1
        elif self.op == "AND":
            self.input_connectors[0].on = self.output_connectors[0].on == 1 and self.output_connectors[1].on == 1
        elif self.op == "XOR":
            self.input_connectors[0].on = (self.output_connectors[0].on == 1) != (self.output_connectors[1].on == 1)
        elif self.op == "IMP":
            self.input_connectors[0].on = self.output_connectors[0].on == 0 or self.output_connectors[1].on == 1
        elif self.op == "NOR":
            self.input_connectors[0].on = not (self.output_connectors[0].on == 1 or self.output_connectors[1].on == 1)
        elif self.op == "NAND":
            self.input_connectors[0].on = not (self.output_connectors[0].on == 1 and self.output_connectors[1].on == 1)
        elif self.op == "XNOR":
            self.input_connectors[0].on = not ((self.output_connectors[0].on == 1) != (self.output_connectors[1].on == 1))
        elif self.op == "NIMP":
            self.input_connectors[0].on = not (self.output_connectors[0].on == 0 or self.output_connectors[1].on == 1)
        elif self.op == "NOT":
            self.input_connectors[0].on = not (self.output_connectors[0].on == 1)
        elif self.op == "YES":
            self.input_connectors[0].on = self.output_connectors[0].on == 1

        self.input_connectors[0].correct_color()
