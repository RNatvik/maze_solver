# Start with an image as shown in generator_base.png
# Use recursive backtracking
from PIL import Image
from src.node import Node
import random


def generate(width, height, output_file):
    if width % 2 == 0:
        width += 1
    if height % 2 == 0:
        height += 1
    if width < 3:
        width = 3
    if height < 3:
        height = 3

    pixel_map = {}
    nodes = {}

    # Create an all black canvas
    for x in range(width):
        for y in range(height):
            pixel_map[(x, y)] = 0

    x_range = int((width - 1) / 2)
    y_range = int((height - 1) / 2)

    # Set start and end locations
    start_loc = (random.randint(0, x_range - 1) * 2 + 1, 0)
    end_loc = (random.randint(0, x_range - 1) * 2 + 1, height - 1)
    pixel_map[start_loc] = 1
    pixel_map[end_loc] = 1

    start = Node(start_loc)
    end = Node(end_loc)

    nodes[start_loc] = start
    nodes[end_loc] = end

    # Place white pixel and nodes on all odd x, y locations
    for x in range(x_range):
        for y in range(y_range):
            pixel = (x * 2 + 1, y * 2 + 1)
            pixel_map[pixel] = 1
            nodes[pixel] = Node(pixel)

    # Connect all nodes to neighbours
    start.add_connection(nodes.get((start_loc[0], start_loc[1] + 1)))
    end.add_connection(nodes.get((end_loc[0], end_loc[1] + -1)))
    for x in range(x_range):
        for y in range(y_range):
            pixel = (x * 2 + 1, y * 2 + 1)
            temp_node = nodes[pixel]
            if pixel[0] + 2 < width:
                temp_node.add_connection(nodes[(pixel[0] + 2, pixel[1])])
            if pixel[1] + 2 < height:
                temp_node.add_connection(nodes[(pixel[0], pixel[1] + 2)])

    # Make path
    visited_nodes = set()
    current_node = nodes[start_loc]
    previous_nodes = []
    while len(visited_nodes) != len(nodes):
        to_be_removed = []
        for connection in current_node.connections:
            if connection in visited_nodes:
                to_be_removed.append(connection)
        for connection in to_be_removed:
            current_node.connections.remove(connection)

        next_node = None
        if len(current_node.connections) > 0:
            random_value = random.randint(0, len(current_node.connections) - 1)
            next_node = current_node.connections[random_value]
            x_value = current_node.position[0]
            y_value = current_node.position[1]

            if current_node.position[0] == next_node.position[0]:  # Vertical line
                y_value = int((next_node.position[1] + current_node.position[1]) / 2)

            elif current_node.position[1] == next_node.position[1]:  # Horizontal line
                x_value = int((next_node.position[0] + current_node.position[0]) / 2)

            pixel_map[(x_value, y_value)] = 1
            previous_nodes.append(current_node)

        else:
            next_node = previous_nodes.pop(-1)

        visited_nodes.add(current_node)
        current_node = next_node

    # Save the maze as .png image
    data = []
    for y in range(height):
        for x in range(width):
            data.append(pixel_map[x, y])

    image = Image.new('P', (width, height))
    image.putpalette([0, 0, 0, 255, 255, 255])
    image.putdata(data)
    image.save(output_file)
