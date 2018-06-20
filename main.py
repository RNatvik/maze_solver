from PIL import Image
from datetime import datetime
import time
from maze import Maze
import simpleSolver


def saveImage(im, result):
    print("Saving Image")
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

    # TODO, make output image dependent on arguments
    destination = "mazes/result/"
    dateTime = datetime.now()
    filename = str(dateTime.date()) + " " + str(dateTime.time()) + ".png"
    im.save(destination + filename)
    print("Image saved in " + destination + " as " + filename)


def main():
    print("Opening image...")

    # TODO, make image dependent on argument
    image = Image.open("mazes/braid200.png")

    print("Analyzing image and creating nodes...")
    startTime = time.time()
    maze = Maze(image)
    endTime = time.time()
    totalTime = endTime - startTime
    print("Maze creation time:", totalTime)
    print("Number of nodes:", len(maze.nodes))

    print("Solving...")
    startTime = time.time()
    path = simpleSolver.solve(maze)
    endTime = time.time()
    totalTime = endTime - startTime
    print("Solve time:", totalTime)

    # TODO, make this segment dependent on arguments
    print("\nPath:")
    for node in path:
        print(node.Position)

    print("\nPath length:", maze.end.distanceToStart)

    saveImage(image, path)


if __name__ == "__main__":
    main()
