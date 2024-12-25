import sys
import os
import pygame
from InputNode import InputNode
from OutputNode import OutputNode
from InputConnector import InputConnector
from OutputConnector import OutputConnector
from Chip import Chip
from Variables import *

os.environ['SDL_AUDIODRIVER'] = 'dsp'

pygame.init()


def invalid_node_build_position(mp):
    for node in nodes:
        is_input_node = isinstance(node, InputNode)
        is_output_node = isinstance(node, OutputNode)

        if abs(mp[1] - node_positions[nodes.index(node)][1]) <= 24 and (
                (mp[0] < 100 and is_input_node) or (mp[0] > width - 100 and is_output_node)):
            return [node, True]

    return [0, False]


nodes = []
node_positions = []
connectors = []
connections = []
chips = []
connect_checks = []
chip_types = ["OR", "AND", "XOR", "IMP", "NOR", "NAND", "XNOR", "NIMP", "NOT", "YES"]

preview_input = False
preview_output = False

check_for_chip_placement = [0, False]

check_for_output_node = False

# "if applicable" refers to if the mouse is in the correct position and if the program is in the correct mode
while True:
    mouse_position = pygame.mouse.get_pos()
    for event in pygame.event.get():
        # Escape key or close program to exit
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            sys.exit()

        # If mouse button is pressed
        if event.type == pygame.MOUSEBUTTONDOWN:
            invalid_position = invalid_node_build_position(mouse_position)
            # If that button is left click
            if pygame.mouse.get_pressed()[0]:
                connect_checks.clear()

                # Create list of the data for each connector representing if it was clicked on by the mouse
                for chip in chips:
                    connect_checks.append(chip.check_for_connection(mouse_position))

                # Turn on input node if applicable
                if invalid_position[1] and mouse_position[0] <= 15:
                    invalid_position[0].flip()

                # Create a wire to an output node if applicable
                elif check_for_output_node and width - 15 > mouse_position[0] >= width - 34 and invalid_position[1]:
                    input_count = 0
                    for connection in connections:
                        if connection[3] == invalid_position[0]:
                            input_count += 1
                    if input_count < 1:
                        output_position = node_positions[nodes.index(invalid_position[0])]
                        connections.append([input_connector, input_position[1], output_position, invalid_position[0]])

                for check in connect_checks:

                    # Create a wire to an input connector if applicable
                    if check_for_output_node and check[1] and check[2]:
                        input_count = 0
                        for connection in connections:
                            if connection[3] == check[0]:
                                input_count += 1
                        if input_count < 1:
                            output_position = chips[connect_checks.index(check)].output_connector_positions[
                                chips[connect_checks.index(check)].output_connectors.index(check[0])]
                            connections.append([input_connector, input_position[1], output_position, check[0]])

                    # Remove a wire to an input connector if applicable
                    elif not check_for_output_node and check[1]:
                        for connection in connections:
                            if connection[3] == check[0]:
                                check[0].on = 0
                                connection[3].on = 0
                                connection[3].correct_color()
                                connections.remove(connection)

                # Remove a wire to an output node if applicable
                if not check_for_output_node and width - 15 > mouse_position[0] >= width - 34 and invalid_position[1]:
                    for connection in connections:
                        if connection[3] == invalid_position[0]:
                            connectors[nodes.index(connection[3])].on = 0
                            connection[3].on = 0
                            connection[3].correct_color()
                            connections.remove(connection)
                if check_for_output_node:
                    check_for_output_node = False

                # On the next click of the left mouse button, a wire may be created if, on this click, the mouse
                # clicked on an input node or an output connector
                elif invalid_position[1] and (15 < mouse_position[0] <= 34):
                    check_for_output_node = True
                    input_connector = connectors[nodes.index(invalid_position[0])]
                    input_position = node_positions[nodes.index(invalid_position[0])]
                for check in connect_checks:
                    if check[1] and not check[2]:
                        check_for_output_node = True
                        input_connector = check[0]
                        input_position = chips[connect_checks.index(check)].input_connector_positions[
                            chips[connect_checks.index(check)].input_connectors.index(check[0])]

                # Build a new input node if applicable
                if mouse_position[0] < 100 and not invalid_position[1]:
                    node_positions.append(mouse_position)
                    nodes.append(InputNode())
                    connectors.append(InputConnector(29, 10, mouse_position[1], False))

                # Build a new output node if applicable
                elif mouse_position[0] > width - 100 and not invalid_position[1]:
                    node_positions.append([width - 29, mouse_position[1]])
                    nodes.append(OutputNode())
                    connectors.append(OutputConnector(width - 29, 10, mouse_position[1], False))

                # Build a new chip if applicable
                if check_for_chip_placement[1] and not invalid_position[1] and mouse_position[1] < height - 340 \
                        and 100 < mouse_position[0] < width - 100:
                    build = True
                    for chip in chips:
                        if (abs(mouse_position[1] - chip.y) < 30) and (abs(mouse_position[0] - chip.x) < 65):
                            build = False
                    if build:
                        if check_for_chip_placement[0] == "NOT" or check_for_chip_placement[0] == "YES":
                            chips.append(Chip(check_for_chip_placement[0], 1, 1, mouse_position[0], mouse_position[1]))
                        else:
                            chips.append(Chip(check_for_chip_placement[0], 1, 2, mouse_position[0], mouse_position[1]))
                if check_for_chip_placement[1]:
                    check_for_chip_placement = [0, False]

                # On the next click of the left mouse button, a chip may be created if, on this click, the mouse
                # clicked on one of the chips in the chip inventory
                if mouse_position[1] > height - 100:
                    for chip_type in chip_types:
                        if chip_types.index(chip_type) * 100 < mouse_position[0] < chip_types.index(
                                chip_type) * 100 + 100:
                            check_for_chip_placement = [chip_type, True]

            # If that button is middle click
            if pygame.mouse.get_pressed()[1]:

                # If the mouse was over an input node, remove the input node
                if invalid_position[1] and mouse_position[0] <= 15:
                    node_positions.pop(nodes.index(invalid_position[0]))
                    for connection in connections:
                        if connection[0] == connectors[nodes.index(invalid_position[0])]:
                            connection[3].on = 0
                            connection[3].correct_color()
                            connections.remove(connection)

                    connectors.pop(nodes.index(invalid_position[0]))
                    nodes.remove(invalid_position[0])

                if invalid_position[1] and mouse_position[0] >= width - 15:
                    node_positions.pop(nodes.index(invalid_position[0]))
                    for connection in connections:
                        if connection[3] == invalid_position[0]:
                            connection[0].on = 0
                            connection[0].correct_color()
                            connections.remove(connection)

                    connectors.pop(nodes.index(invalid_position[0]))
                    nodes.remove(invalid_position[0])

    # Preview the location of an input or output node, if it can be placed there
    if mouse_position[0] < 100:
        preview_output = False
        preview_input = True
    elif mouse_position[0] > width - 100:
        preview_input = False
        preview_output = True
    else:
        preview_input = False
        preview_output = False

    clock = pygame.time.Clock()
    clock.tick(60)
    screen.fill((0, 0, 50))

    # Draw the chips onto the screen
    for chip in chips:
        chip.draw()
        chip.correct_output()

    # Draw the nodes and node previews onto the screen
    if preview_input:
        pygame.draw.circle(screen, (50, 50, 50), (0, mouse_position[1]), 12)
    elif preview_output:
        pygame.draw.circle(screen, (50, 50, 50), (width, mouse_position[1]), 12)
    for j in range(len(nodes)):
        nodes[j].draw(node_positions[j][1])
        connectors[j].draw()
        connectors[j].on = nodes[j].on
        connectors[j].check_wire()

    # Draw the wires onto the screen
    for chip in chips:
        for connector in chip.input_connectors:
            connector.check_wire()
    for connection in connections:
        connection[0].connect(connection[1], connection[2])
        connection[3].on = connection[0].on
        connection[3].correct_color()
    pygame.draw.rect(screen, (0, 50, 50), (0, height - 100, width, 100))
    pygame.draw.rect(screen, (0, 0, 0), (0, height - 110, width, 10))

    # Change the color of the chip hovered over in the chip inventory, if applicable, and draw the chip inventory
    for chip_type in chip_types:
        color = (50, 50, 50)
        if mouse_position[1] > height - 100:
            if chip_types.index(chip_type) * 100 < mouse_position[0] < chip_types.index(chip_type) * 100 + 100:
                color = (25, 25, 25)
        pygame.draw.rect(screen, color, (chip_types.index(chip_type) * 100, height - 100, 100, 100))
        text = big_font.render(chip_type, True, (255, 255, 255))
        screen.blit(text, (chip_types.index(chip_type) * 100, height - 100))

    pygame.display.update()
