from PIL import Image
from src.maze import Node
import random
import math
from src.maze import Maze
from src.solver import solve_maze
from time import time


def factory(width, height, output_file, method='perfect', text_area=None):
    try:
        # Make width and height odd numbers
        if width % 2 == 0:
            width += 1
        if height % 2 == 0:
            height += 1
        if width < 3:
            width = 3
        if height < 3:
            height = 3

        stats = None

        # Select method of generation
        if method == 'perfect':
            stats = perfect(width, height, output_file)
        elif method == 'braid':
            stats = braid(width, height, output_file)
        elif method == 'branch':
            stats = branching(width, height, output_file)

        # Display message
        if text_area is not None:
            text_area.config(state='normal')
            text_area.insert('end', "\nMaze generation complete!")
            text_area.insert('end', "\nGeneration time: " + str(stats) + "\n")
            text_area.config(state='disabled')
            text_area.see('end')
        else:
            print("Maze generation complete!")
            print("Generation time: ", stats)
            print()

    except FileNotFoundError as e:
        if text_area is not None:
            message = "\nERROR!: \n{}: {}\n"
            message = message.format(e.strerror, e.filename)
            text_area.config(state='normal')
            text_area.insert('end', message)
            text_area.config(state='disabled')
            text_area.see('end')
        else:
            message = "\nERROR!: \n{}: {}\n"
            message = message.format(e.strerror, e.filename)
            print(message)


def timed(func):
    def timed_method(*args, **kwargs):
        start_time = time()
        func(*args, **kwargs)
        end_time = time()
        total_time = end_time - start_time
        return total_time
    return timed_method


@timed
def perfect(width, height, output_file):
    # setup
    start, end, nodes, pixel_map = setup(width, height)
    # Make path
    pixel_map = make_basic_path(nodes, start, pixel_map)
    # Save the maze as .png image
    make_image(pixel_map, width, height, output_file=output_file)


@timed
def braid(width, height, output_file):
    # setup
    start, end, nodes, pixel_map = setup(width, height)

    # Make path
    visited_nodes = set()
    current_node = nodes[start.position]
    previous_nodes = []
    banned_node = None
    ignore_visited = False
    ignore_chance = int(math.sqrt((width + height) / 2) * 1)

    while len(visited_nodes) != len(nodes):
        to_be_removed = []
        connections = list(current_node.connections)
        if not ignore_visited:
            for connection in connections:
                if connection in visited_nodes:
                    to_be_removed.append(connection)
            for connection in to_be_removed:
                connections.remove(connection)
        else:
            ignore_visited = False
            connections.remove(banned_node)

        next_node = None
        if len(connections) > 0:
            random_value = random.randint(0, len(connections) - 1)
            next_node = connections[random_value]
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

            ignore_value = random.randint(0, ignore_chance)
            if ignore_value == 0:
                ignore_visited = True
                banned_node = current_node

        visited_nodes.add(current_node)
        current_node = next_node

    # Save the maze as .png image
    make_image(pixel_map, width, height, output_file=output_file)


@timed
def branching(width, height, output_file):

    # setup
    start, end, nodes, pixel_map = setup(width, height)

    # Make path
    pixel_map = make_basic_path(nodes, start, pixel_map)

    # Make temporary image
    image = make_image(pixel_map, width, height)

    # Solve maze to find solution path and later remove random wall nodes along the path
    maze = Maze(image)
    (path, considered_nodes, visited_nodes) = solve_maze(maze)

    for node in path:
        if node is not start and node is not end:
            random_value = random.randint(0, 10)
            if random_value is 0:
                x_value = node.position[0]
                y_value = node.position[1]
                random_value = random.randint(0, 3)
                if random_value is 0: # Break left wall
                    pixel_map[(x_value - 1, y_value)] = 1
                elif random_value is 1: # Break south wall
                    pixel_map[(x_value, y_value + 1)] = 1
                elif random_value is 2: # Break east wall
                    pixel_map[(x_value + 1, y_value)] = 1
                elif random_value is 3: # Break north wall
                    pixel_map[(x_value, y_value - 1)] = 1

    for x in range(width):
        pixel_map[(x, 0)] = 0
        pixel_map[(x, height - 1)] = 0
    for y in range(height):
        pixel_map[(0, y)] = 0
        pixel_map[(width - 1, y)] = 0
    pixel_map[start.position] = 1
    pixel_map[end.position] = 1

    make_image(pixel_map, width, height, output_file=output_file)


def make_image(pixel_map: dict, width: int, height: int, output_file=None):
    data = []
    for y in range(height):
        for x in range(width):
            data.append(pixel_map[x, y])

    image = Image.new('P', (width, height))
    image.putpalette([0, 0, 0, 255, 255, 255])
    image.putdata(data)
    if output_file is not None:
        image.save(output_file)
    return image


def make_basic_path(nodes, start, pixel_map):
    # Make path
    visited_nodes = set()
    current_node = nodes[start.position]
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
    return pixel_map


def setup(width, height):

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

    return start, end, nodes, pixel_map
