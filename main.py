from PIL import Image
import time
import argparse
from maze import Maze
from node import Node
import simpleSolver


def saveImage(im, result, output_file):
    print("\nSaving Image...")
    im = im.convert('RGB')
    impixels = im.load()

    resultpath = [n.Position for n in result]

    length = len(resultpath)

    for i in range(0, length - 1):
        a = resultpath[i]
        b = resultpath[i + 1]

        # Blue - red
        r = int((i / length) * 255)
        px = (r, 0, 255 - r)

        if a[0] == b[0]:
            # X equal, vertical line
            for x in range(min(a[1], b[1]), max(a[1], b[1]) + 1):
                impixels[a[0], x] = px
        elif a[1] == b[1]:
            # Y equal, horizontal line
            for y in range(min(a[0], b[0]), max(a[0], b[0]) + 1):
                impixels[y, a[1]] = px

    im.save(output_file)
    outputTree = output_file.split("/")
    filename = outputTree[len(outputTree) - 1]
    destination = ""
    for i in range(len(outputTree) - 1):
        destination += outputTree[i] + "/"

    print("Image saved in " + destination + " as " + filename)


def main(input_file, output_file, show_path):
    # work_state indicates which parts of the code is being executed
    work_state = int()

    try:
        work_state = 0
        print("Opening image...")
        image = Image.open(input_file)

        work_state = 1
        print("Analyzing image and creating nodes...")
        startTime = time.time()
        maze = Maze(image)
        endTime = time.time()
        totalTime = endTime - startTime
        print("Maze creation time:", totalTime)
        print("Number of nodes:", len(maze.nodes))

        work_state = 2
        print("Solving...")
        startTime = time.time()
        (path, consideredNodes, visitedNodes) = simpleSolver.solve(maze)
        endTime = time.time()
        totalTime = endTime - startTime

        work_state = 3
        if show_path is True:
            print("\nPath:")
            for node in path:
                print(node.Position)

        work_state = 4
        print("Solve time:", totalTime)
        print("\nVisited nodes:", visitedNodes)
        print("Considered nodes:", consideredNodes)
        print("Path pixel length:", int(maze.end.distanceToStart))
        print("Path node length:", len(path))
        print("DTE Weight:", Node.weight)

        saveImage(image, path, output_file)

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
        elif work_state == 4:
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

    parser.add_argument("--showPath",
                        help="Print the path in terminal (default is False)",
                        choices=["true", "false"])

    parser.add_argument("--weight",
                        type=int,
                        help="A number indicating the weight of distance to end when prioritizing nodes (default is 1)",
                        choices=[0, 1, 2, 3, 4, 5])

    args = parser.parse_args()
    input_file = args.input
    output_file = args.output
    show_path = args.showPath
    weight = args.weight
    if show_path is None:
        show_path = False
    if weight is None:
        weight = 1

    Node.weight = weight
    main(input_file, output_file, show_path)
