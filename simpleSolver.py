# Solves the maze by creating a priority queue of nodes, starting with the start node at distance 0
# then adding the pixel distance to the next node IN THE NEXT NODE
# To retrace, take the end node, and go to the connection with the shortest distance to start. Repeat until distance to
# start == 0
import math


def solve(maze):
    start = maze.start
    end = maze.end
    visitedNodes = []
    start.distanceToStart = 0
    priorityQueue = []
    priorityQueue.append(start)

    while priorityQueue[0] != end:
        currentNode = priorityQueue[0]
        currentConnections = list(currentNode.Connections)
        while None in currentConnections:
            currentConnections.remove(None)
        for nextNode in currentConnections:
            if not visitedNodes.__contains__(nextNode):

                distance = 0

                if nextNode.Position[0] == currentNode.Position[0]:  # X equal, vertical line
                    # Calculates the square root of the difference between current and next Y squared
                    distance = math.sqrt(math.pow((nextNode.Position[1] - currentNode.Position[1]), 2))
                    distance += currentNode.distanceToStart

                elif nextNode.Position[1] == currentNode.Position[1]:  # Y equal, horizontal line
                    # Calculates the square root of the difference between current and next Y squared
                    distance = math.sqrt(math.pow((nextNode.Position[0] - currentNode.Position[0]), 2))
                    distance += currentNode.distanceToStart

                if priorityQueue.__contains__(nextNode):
                    if nextNode.distanceToStart > distance:
                        nextNode.distanceToStart = distance

                else:
                    nextNode.distanceToStart = distance
                    priorityQueue.append(nextNode)

        visitedNodes.append(currentNode)
        priorityQueue.remove(currentNode)
        priorityQueue.sort()

    path = []
    pathNode = end
    path.append(pathNode)

    while pathNode != start:
        connections = list(pathNode.Connections)
        while None in connections:
            connections.remove(None)
        # Set distance to end in relevant nodes to 0, as the goal is to find shortest path to start
        for connection in connections:
            connection.distanceToEnd = 0
        connections.sort()
        pathNode = connections[0]
        path.append(pathNode)

    path.sort()
    return path
