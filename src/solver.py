from PIL import Image
import time
import math
import heapq
from src.maze import Maze, Node
from tkinter import Text, END


def main(text_area: Text, input_file: str, output_file: str, save_visited_nodes: bool, show_path: bool):
    work_state = int()
    try:
        work_state = 0
        insert_text(text_area, "\nOpening image...")
        image = Image.open(input_file)

        work_state = 1
        insert_text(text_area, "\nAnalyzing image and creating nodes...")
        start_time = time.time()
        maze = Maze(image)
        end_time = time.time()
        total_time = end_time - start_time
        insert_text(text_area, "\nMaze creation time: {}".format(total_time))
        insert_text(text_area, "\nNumber of nodes: {}".format(len(maze.nodes)))

        work_state = 2
        insert_text(text_area, "\nSolving...")
        start_time = time.time()
        (path, considered_nodes, visited_nodes) = solve_maze(maze)
        end_time = time.time()
        total_time = end_time - start_time

        work_state = 3
        if show_path:
            insert_text(text_area, "\n\nPath:")
            for node in path:
                insert_text(text_area, "\n{}".format(node.position))

        insert_text(text_area, "\nSolve time: {}".format(total_time))
        insert_text(text_area, "\n\nVisited nodes: {}".format(len(visited_nodes)))
        insert_text(text_area, "\nConsidered nodes: {}".format(considered_nodes))
        insert_text(text_area, "\nPath pixel length: {}".format(int(maze.end.distance_to_start)))
        insert_text(text_area, "\nPath node length: {}".format(len(path)))
        insert_text(text_area, "\nDTE Weight: {}".format(Node.weight))

        work_state = 4
        if save_visited_nodes:
            image = paint_nodes(image, visited_nodes)

        work_state = 5
        save_image(text_area, image, path, output_file)

    except AttributeError:
        if work_state == 1:
            insert_text(text_area, "\nSomething went wrong when loading the maze to memory."
                                   "\n   Please make sure maze is of the proper format")
        elif input_file == "":
            insert_text(text_area, "\nPlease specify input image before attempting solve")
        else:
            insert_text(text_area, "\nAn AttributeError has been raised unexpectedly... please contact support"
                                   "\n   work_state = " + str(work_state))

    except FileNotFoundError:
        if work_state == 0:
            insert_text(text_area, "\nInput image was not found."
                                   "\n   Please make sure you have specified the right folder and file")
        elif work_state == 5:
            insert_text(text_area, "\nOutput folder or file was not found"
                                   "\n   Please make sure you have specified a valid folder")
        else:
            insert_text(text_area, "\nA FileNotFoundError was raised unexpectedly... please contact support"
                                   "\n   work_state = " + str(work_state))

    except IndexError:
        if work_state == 2:
            insert_text(text_area, "\nMaze has no solution")
        else:
            insert_text(text_area, "\nAn unexpected IndexError was raised... please contact support"
                                   "\n   work_state = " + str(work_state))


def solve_maze(maze):

    start = maze.start
    end = maze.end
    visited_nodes = set()
    start.distance_to_start = 0
    priority_queue = [start]
    heapq.heapify(priority_queue)

    considered_nodes = 0

    while priority_queue[0] != end:
        current_node = heapq.heappop(priority_queue)
        current_connections = set(current_node.connections)

        for next_node in current_connections:
            if next_node not in visited_nodes:
                considered_nodes += 1

                distance = 0
                if next_node.position[0] == current_node.position[0]:  # X equal, vertical line
                    # Calculates the square root of the difference between current and next Y squared
                    distance = math.sqrt(math.pow((next_node.position[1] - current_node.position[1]), 2))
                    distance += current_node.distance_to_start

                elif next_node.position[1] == current_node.position[1]:  # Y equal, horizontal line
                    # Calculates the square root of the difference between current and next Y squared
                    distance = math.sqrt(math.pow((next_node.position[0] - current_node.position[0]), 2))
                    distance += current_node.distance_to_start

                if next_node in priority_queue:
                    if next_node.distance_to_start > distance:
                        next_node.distance_to_start = distance

                else:
                    next_node.distance_to_start = distance
                    heapq.heappush(priority_queue, next_node)

        visited_nodes.add(current_node)

    path_node = end
    path = [path_node]

    while path_node != start:
        connections = list(path_node.connections)
        # Set distance to end in relevant nodes to 0, as the goal is to find shortest path to start
        for connection in connections:
            connection.distance_to_end = 0
        connections.sort()
        path_node = connections[0]
        path.append(path_node)

    path.sort()
    return path, considered_nodes, visited_nodes


def save_image(text_area: Text, image: Image, result: list, output_file: str):
    insert_text(text_area, "\n\nSaving Image...")
    image = image.convert('RGB')
    image_pixels = image.load()
    result_path = [n.position for n in result]

    length = len(result_path)

    for i in range(0, length - 1):
        a = result_path[i]
        b = result_path[i + 1]

        # Blue - red
        r = int((i / length) * 255)
        px = (r, 0, 255 - r)

        if a[0] == b[0]:
            # X equal, vertical line
            for x in range(min(a[1], b[1]), max(a[1], b[1]) + 1):
                image_pixels[a[0], x] = px
        elif a[1] == b[1]:
            # Y equal, horizontal line
            for y in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
                image_pixels[y, a[1]] = px

    image.save(output_file)

    output_tree = output_file.split("/")
    filename = output_tree[len(output_tree) - 1]
    destination = ""
    for i in range(len(output_tree) - 1):
        destination += output_tree[i] + "/"
    insert_text(text_area, "\nImage saved in " + destination + " as " + filename + "\n")


def paint_nodes(image: Image, nodes: set):
    color = (0, 255, 0)
    image = image.convert('RGB')
    image_pixels = image.load()
    for node in nodes:
        image_pixels[node.position] = color
    return image


def insert_text(text_area: Text, message: str):
    text_area.config(state='normal')
    text_area.insert(END, message)
    text_area.see(END)
    text_area.config(state='disabled')
