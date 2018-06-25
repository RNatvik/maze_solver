import math


class Node:

    weight = 1

    def __init__(self, position):
        self.position = position
        self.connections = set()
        self.distance_to_start = None
        self.distance_to_end = None

    def set_distance_to_end(self, end_node):
        x = math.sqrt(math.pow((self.position[0] - end_node.position[0]), 2))
        y = math.sqrt(math.pow((self.position[1] - end_node.position[1]), 2))
        self.distance_to_end = x + y

    # use Node.left, Node.right, Node.up, and Node.down to indicate direction
    def add_connection(self, node):
        self.connections.add(node)
        node.connections.add(self)

    # This makes it so that when sorting a list of Node objects, they are listed in order of distance to start
    def __lt__(self, other):
        self_distance = self.distance_to_start
        other_distance = other.distance_to_start
        if (self_distance is not None) and (other_distance is not None):
            self_distance += int(self.distance_to_end * Node.weight)
            other_distance += int(other.distance_to_end * Node.weight)
        else:
            if self_distance is None:
                self_distance = 100000000
            if other_distance is None:
                other_distance = 100000000
        return self_distance < other_distance

