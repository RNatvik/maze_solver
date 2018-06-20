from node import Node


class Maze:

    def __init__(self, image):
        width = image.size[0]
        height = image.size[1]

        topNodes = [None] * width
        data = list(image.getdata(0))
        # This will result in a 1 dimensional list of 1 and 0, where 1 is path and 0 is wall

        self.start = None
        self.end = None
        #### Testing ####
        self.nodes = []

        # Find the start node
        for x in range(0, width):
            if data[x] == 1:
                self.start = Node((x, 0))
                topNodes[x] = self.start
                #### Testing ####
                self.nodes.append(self.start)
                break

        for y in range(1, height - 1):

            offset = y * width
            previousX = data[offset]
            leftNode = None

            for x in range(0, width):
                index = offset + x

                currentX = data[index]
                nextX = data[index + 1]

                # PATH WALL PATH
                # PATH WALL WALL
                # WALL WALL PATH
                # WALL WALL WALL
                if currentX == 0:
                    previousX = currentX
                    topNodes[x] = None
                    leftNode = None
                    continue
                else:
                    # PATH PATH PATH
                    if previousX == 1 and nextX == 1:
                        above = data[index - width]
                        below = data[index + width]
                        if (below == 1) or (above == 1):
                            node = Node((x, y))
                            node.addConnection(Node.left, leftNode)

                            if above == 1:
                                node.addConnection(Node.up, topNodes[x])

                            if below == 1:
                                topNodes[x] = node

                            leftNode = node
                            #### Testing ####
                            self.nodes.append(node)

                    # WALL PATH PATH (start of corridor)
                    elif previousX == 0 and nextX == 1:
                        node = Node((x, y))

                        above = data[index - width]
                        below = data[index + width]

                        if above == 1:
                            node.addConnection(Node.up, topNodes[x])

                        if below == 1:
                            topNodes[x] = node

                        leftNode = node
                        #### Testing ####
                        self.nodes.append(node)

                    # PATH PATH WALL (end of corridor)
                    elif previousX == 1 and nextX == 0:
                        node = Node((x, y))
                        node.addConnection(Node.left, leftNode)
                        above = data[index - width]
                        below = data[index + width]

                        if above == 1:
                            node.addConnection(Node.up, topNodes[x])

                        if below == 1:
                            topNodes[x] = node
                        #### Testing ####
                        self.nodes.append(node)

                    # WALL PATH WALL
                    elif previousX == 0 and nextX == 0:
                        above = data[index - width]
                        below = data[index + width]

                        if ((above == 0) + (below == 0)) == 1:
                            node = Node((x, y))

                            if above == 1:
                                node.addConnection(Node.up, topNodes[x])
                            elif below == 1:
                                topNodes[x] = node

                            #### Testing ####
                            self.nodes.append(node)
                previousX = currentX

        # Find the end node
        offset = (height - 1) * width
        for x in range(0, width):
            index = offset + x
            if data[index] == 1:
                self.end = Node((x, height - 1))
                self.end.addConnection(Node.up, topNodes[x])
                #### Testing ####
                self.nodes.append(self.end)
                break

