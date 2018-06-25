# Solves the maze by creating a priority queue of nodes, starting with the start node at distance 0
# then adding the pixel distance to the next node IN THE NEXT NODE
# To retrace, take the end node, and go to the connection with the shortest distance to start. Repeat until distance to
# start == 0
import math
import heapq


def solve(maze):

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
        while None in current_connections:
            current_connections.remove(None)

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
        while None in connections:
            connections.remove(None)
        # Set distance to end in relevant nodes to 0, as the goal is to find shortest path to start
        for connection in connections:
            connection.distance_to_end = 0
        connections.sort()
        path_node = connections[0]
        path.append(path_node)

    path.sort()
    return path, considered_nodes, len(visited_nodes)
