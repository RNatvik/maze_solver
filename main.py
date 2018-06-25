from PIL import Image
import time
import argparse
from maze import Maze
from node import Node
import simpleSolver


def save_image(image, result, output_file):
    print("\nSaving Image...")
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
    print("Image saved in " + destination + " as " + filename)


def paint_nodes(image, nodes):
    color = (0, 255, 0)
    image = image.convert('RGB')
    image_pixels = image.load()
    for node in nodes:
        image_pixels[node.position] = color
    return image


def main(input_file, output_file, save_visited_nodes, show_path):

    work_state = int()
    try:
        work_state = 0
        print("Opening image...")
        image = Image.open(input_file)

        work_state = 1
        print("Analyzing image and creating nodes...")
        start_time = time.time()
        maze = Maze(image)
        end_time = time.time()
        total_time = end_time - start_time
        print("Maze creation time:", total_time)
        print("Number of nodes:", len(maze.nodes))

        work_state = 2
        print("Solving...")
        start_time = time.time()
        (path, considered_nodes, visited_nodes) = simpleSolver.solve(maze)
        end_time = time.time()
        total_time = end_time - start_time

        work_state = 3
        if show_path:
            print("\nPath:")
            for node in path:
                print(node.position)

        print("Solve time:", total_time)
        print("\nVisited nodes:", len(visited_nodes))
        print("Considered nodes:", considered_nodes)
        print("Path pixel length:", int(maze.end.distance_to_start))
        print("Path node length:", len(path))
        print("DTE Weight:", Node.weight)

        work_state = 4
        if save_visited_nodes:
            image = paint_nodes(image, visited_nodes)

        work_state = 5
        save_image(image, path, output_file)

    except AttributeError:
        if work_state == 1:
            print("Something went wrong when loading the maze to memory."
                  "\n   Please make sure maze is of the proper format")
        else:
            print("An AttributeError has been raised unexpectedly... please contact support"
                  "\n   work_state = " + str(work_state))

    except FileNotFoundError:
        if work_state == 0:
            print("Input image was not found."
                  "\n   Please make sure you have specified the right folder and file")
        elif work_state == 5:
            print("Output folder or file was not found"
                  "\n   Please make sure you have specified a valid folder and have given the file the extension .png")
        else:
            print("A FileNotFoundError was raised unexpectedly... please contact support"
                  "\n   work_state = " + str(work_state))

    except IndexError:
        if work_state == 2:
            print("Maze has no solution")
        else:
            print("An unexpected IndexError was raised... please contact support"
                  "\n   work_state = " + str(work_state))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("input",
                        help="the input image file of the maze")

    parser.add_argument("output",
                        help="the output image file")

    parser.add_argument("--sp",
                        type=bool,
                        help="Show the path as text in terminal (default is False)",
                        choices=[True, False])

    parser.add_argument("--svn",
                        type=bool,
                        help="Save visited nodes as green pixels in output file (default is False)",
                        choices=[True, False])

    parser.add_argument("--weight",
                        type=float,
                        help="A number indicating the weight of distance to end when prioritizing nodes (default is 1)")

    args = parser.parse_args()
    input_file = args.input
    output_file = args.output
    show_path = args.sp
    save_visited_nodes = args.svn
    weight = args.weight

    if show_path is None:
        show_path = False
    if save_visited_nodes is None:
        save_visited_nodes = False
    if weight is not None:
        Node.weight = weight

    main(input_file, output_file, save_visited_nodes, show_path)
