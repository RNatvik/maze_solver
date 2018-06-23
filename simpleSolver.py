# Solves the maze by creating a priority queue of nodes, starting with the start node at distance 0
# then adding the pixel distance to the next node IN THE NEXT NODE
# To retrace, take the end node, and go to the connection with the shortest distance to start. Repeat until distance to
# start == 0
import math
import heapq


def solve(maze):

    start = maze.start
    end = maze.end
    visitedNodes = set()
    start.distanceToStart = 0
    priorityQueue = []
    priorityQueue.append(start)
    heapq.heapify(priorityQueue)

    count0 = 0
    count1 = 0
    count2 = 0

    while priorityQueue[0] != end:
        count0 += 1
        currentNode = heapq.heappop(priorityQueue)
        currentConnections = set(currentNode.Connections)
        while None in currentConnections:
            currentConnections.remove(None)
        for nextNode in currentConnections:
            count1 += 1
            if nextNode not in visitedNodes:
                count2 += 1

                distance = 0
                if nextNode.Position[0] == currentNode.Position[0]:  # X equal, vertical line
                    # Calculates the square root of the difference between current and next Y squared
                    distance = math.sqrt(math.pow((nextNode.Position[1] - currentNode.Position[1]), 2))
                    distance += currentNode.distanceToStart

                elif nextNode.Position[1] == currentNode.Position[1]:  # Y equal, horizontal line
                    # Calculates the square root of the difference between current and next Y squared
                    distance = math.sqrt(math.pow((nextNode.Position[0] - currentNode.Position[0]), 2))
                    distance += currentNode.distanceToStart

                if nextNode in priorityQueue:
                    if nextNode.distanceToStart > distance:
                        nextNode.distanceToStart = distance

                else:
                    nextNode.distanceToStart = distance
                    heapq.heappush(priorityQueue, nextNode)


        visitedNodes.add(currentNode)

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
    print("While loop iterations:", count0)
    print("Connections checked:", count1)
    print("Not visited connections checked:", count2)
    print("Visited nodes:", len(visitedNodes))
    print("Prio queue length:", len(priorityQueue))
    return path
