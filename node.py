import math


class Node:

    left = 0
    down = 1
    right = 2
    up = 3

    def __init__(self, position):
        self.Position = position
        self.Connections = [None] * 4
        self.distanceToStart = None
        self.distanceToEnd = None

    def setDistanceToEnd(self, endNode):
        x = math.pow(endNode.Position[0] - self.Position[0], 2)
        y = math.pow(endNode.Position[1] - self.Position[1], 2)
        self.distanceToEnd = int(math.sqrt(x + y))


    # Direction is an integer 0-3 (inclusive), 0 is left, 1 is down, 2 is right, 3 is up
    # Can also use Node.left, Node.right, Node.up, and Node.down to indicate direction
    def addConnection(self, direction, node):
        self.Connections[direction] = node

        if direction == Node.left:
            node.Connections[Node.right] = self

        elif direction == Node.right:
            node.Connections[Node.left] = self

        elif direction == Node.down:
            node.Connections[Node.up] = self

        elif direction == Node.up:
            node.Connections[Node.down] = self

    # This makes it so that when sorting a list of Node objects, they are listed in order of distance to start
    def __lt__(self, other):
        selfDistance = self.distanceToStart
        otherDistance = other.distanceToStart
        if (selfDistance is not None) and (otherDistance is not None):
            selfDistance += self.distanceToEnd
            otherDistance += other.distanceToEnd
        else:
            if selfDistance is None:
                selfDistance = 1000000000
            if otherDistance is None:
                otherDistance = 1000000000
        return selfDistance < otherDistance

