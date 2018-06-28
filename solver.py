from PIL import Image
import time
from maze import Maze
from node import Node
import simpleSolver
from tkinter import Text, END


def save_image(text_area: Text, image: Image, result: list, output_file: str):
    text_area.insert(END, "\n\nSaving Image...")
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
    text_area.insert(END, "\nImage saved in " + destination + " as " + filename)


def paint_nodes(image: Image, nodes: list):
    color = (0, 255, 0)
    image = image.convert('RGB')
    image_pixels = image.load()
    for node in nodes:
        image_pixels[node.position] = color
    return image


def main(text_area: Text, input_file: str, output_file: str, save_visited_nodes: bool, show_path: bool):
    work_state = int()
    try:
        work_state = 0
        text_area.insert(END, "\nOpening image...")
        image = Image.open(input_file)

        work_state = 1
        text_area.insert(END, "\nAnalyzing image and creating nodes...")
        start_time = time.time()
        maze = Maze(image)
        end_time = time.time()
        total_time = end_time - start_time
        text_area.insert(END, "\nMaze creation time: {}".format(total_time))
        text_area.insert(END, "\nNumber of nodes: {}".format(len(maze.nodes)))

        work_state = 2
        text_area.insert(END, "\nSolving...")
        start_time = time.time()
        (path, considered_nodes, visited_nodes) = simpleSolver.solve(maze)
        end_time = time.time()
        total_time = end_time - start_time

        work_state = 3
        if show_path:
            text_area.insert(END, "\n\nPath:")
            for node in path:
                text_area.insert(END, "\n{}".format(node.position))

        text_area.insert(END, "\nSolve time: {}".format(total_time))
        text_area.insert(END, "\n\nVisited nodes: {}".format(len(visited_nodes)))
        text_area.insert(END, "\nConsidered nodes: {}".format(considered_nodes))
        text_area.insert(END, "\nPath pixel length: {}".format(int(maze.end.distance_to_start)))
        text_area.insert(END, "\nPath node length: {}".format(len(path)))
        text_area.insert(END, "\nDTE Weight: {}".format(Node.weight))

        work_state = 4
        if save_visited_nodes:
            image = paint_nodes(image, visited_nodes)

        work_state = 5
        save_image(text_area, image, path, output_file)

    except AttributeError:
        if work_state == 1:
            text_area.insert(END, "\nSomething went wrong when loading the maze to memory."
                                  "\n   Please make sure maze is of the proper format")
        else:
            text_area.insert(END, "\nAn AttributeError has been raised unexpectedly... please contact support"
                                  "\n   work_state = " + str(work_state))

    except FileNotFoundError:
        if work_state == 0:
            text_area.insert(END, "\nInput image was not found."
                                  "\n   Please make sure you have specified the right folder and file")
        elif work_state == 5:
            text_area.insert(END, "\nOutput folder or file was not found"
                                  "\n   Please make sure you have specified a valid folder and "
                                  "have given the file the extension .png")
        else:
            text_area.insert(END, "\nA FileNotFoundError was raised unexpectedly... please contact support"
                                  "\n   work_state = " + str(work_state))

    except IndexError:
        if work_state == 2:
            text_area.insert(END, "\nMaze has no solution")
        else:
            text_area.insert(END, "\nAn unexpected IndexError was raised... please contact support"
                                  "\n   work_state = " + str(work_state))
