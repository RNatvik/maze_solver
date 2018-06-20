# Solves the maze by creating a priority queue of nodes, starting with the start node at distance 0
# then adding the pixel distance to the next node IN THE NEXT NODE
# To retrace, take the end node, and go to the connection with the shortest distance to start. Repeat until distance to
# start == 0
from node import Node


def solve(maze):

    start = maze.start
    end = maze.end
    nodes = maze.nodes
    visitedNodes = []
    start.distanceToStart = 0
    priorityQueue = list(nodes)
    priorityQueue.sort()

    while priorityQueue[0] != end:
        currentNode = priorityQueue[0]

        if currentNode.Connections[Node.left] is not None:
            if not visitedNodes.__contains__(currentNode.Connections[Node.left]):
                nextNode = currentNode.Connections[Node.left]
                distance = currentNode.Position[0] - nextNode.Position[0] + currentNode.distanceToStart
                if nextNode.distanceToStart is None:
                    nextNode.distanceToStart = distance
                else:
                    if nextNode.distanceToStart > distance:
                        nextNode.distanceToStart = distance

        if currentNode.Connections[Node.right] is not None:
            if not visitedNodes.__contains__(currentNode.Connections[Node.right]):
                nextNode = currentNode.Connections[Node.right]
                distance = nextNode.Position[0] - currentNode.Position[0] + currentNode.distanceToStart
                if nextNode.distanceToStart is None:
                    nextNode.distanceToStart = distance
                else:
                    if nextNode.distanceToStart > distance:
                        nextNode.distanceToStart = distance

        if currentNode.Connections[Node.up] is not None:
            if not visitedNodes.__contains__(currentNode.Connections[Node.up]):
                nextNode = currentNode.Connections[Node.up]
                distance = currentNode.Position[1] - nextNode.Position[1] + currentNode.distanceToStart
                if nextNode.distanceToStart is None:
                    nextNode.distanceToStart = distance
                else:
                    if nextNode.distanceToStart > distance:
                        nextNode.distanceToStart = distance

        if currentNode.Connections[Node.down] is not None:
            if not visitedNodes.__contains__(currentNode.Connections[Node.down]):
                nextNode = currentNode.Connections[Node.down]
                distance = nextNode.Position[1] - currentNode.Position[1] + currentNode.distanceToStart
                if nextNode.distanceToStart is None:
                    nextNode.distanceToStart = distance
                else:
                    if nextNode.distanceToStart > distance:
                        nextNode.distanceToStart = distance

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
            a = 1 # this is for debug purpose
            connection.distanceToEnd = 0
        connections.sort()
        pathNode = connections[0]
        path.append(pathNode)

    path.sort()
    return path

