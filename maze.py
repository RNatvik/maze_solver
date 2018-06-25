from node import Node


class Maze:

    def __init__(self, image):
        width = image.size[0]
        height = image.size[1]

        top_nodes = [None] * width
        data = list(image.getdata(0))
        # This will result in a 1 dimensional list of 1 and 0, where 1 is path and 0 is wall

        self.start = None
        self.end = None
        self.nodes = set()

        # Find the start node
        for x in range(0, width):
            if data[x] == 1:
                self.start = Node((x, 0))
                top_nodes[x] = self.start
                self.nodes.add(self.start)
                break

        for y in range(1, height - 1):

            offset = y * width
            previous_x = data[offset]
            left_node = None

            for x in range(0, width):
                index = offset + x

                current_x = data[index]
                next_x = data[index + 1]

                # PATH WALL PATH
                # PATH WALL WALL
                # WALL WALL PATH
                # WALL WALL WALL
                if current_x == 0:
                    previous_x = current_x
                    top_nodes[x] = None
                    left_node = None
                    continue
                else:
                    # PATH PATH PATH
                    if previous_x == 1 and next_x == 1:
                        above = data[index - width]
                        below = data[index + width]
                        if (below == 1) or (above == 1):
                            node = Node((x, y))
                            node.add_connection(left_node)

                            if above == 1:
                                node.add_connection(top_nodes[x])

                            if below == 1:
                                top_nodes[x] = node

                            left_node = node
                            self.nodes.add(node)

                    # WALL PATH PATH (start of corridor)
                    elif previous_x == 0 and next_x == 1:
                        node = Node((x, y))

                        above = data[index - width]
                        below = data[index + width]

                        if above == 1:
                            node.add_connection(top_nodes[x])

                        if below == 1:
                            top_nodes[x] = node

                        left_node = node
                        self.nodes.add(node)

                    # PATH PATH WALL (end of corridor)
                    elif previous_x == 1 and next_x == 0:
                        node = Node((x, y))
                        node.add_connection(left_node)
                        above = data[index - width]
                        below = data[index + width]

                        if above == 1:
                            node.add_connection(top_nodes[x])

                        if below == 1:
                            top_nodes[x] = node
                        self.nodes.add(node)

                    # WALL PATH WALL
                    elif previous_x == 0 and next_x == 0:
                        above = data[index - width]
                        below = data[index + width]

                        if ((above == 0) + (below == 0)) == 1:
                            node = Node((x, y))

                            if above == 1:
                                node.add_connection(top_nodes[x])
                            elif below == 1:
                                top_nodes[x] = node
                            self.nodes.add(node)

                previous_x = current_x

        # Find the end node
        offset = (height - 1) * width
        for x in range(0, width):
            index = offset + x
            if data[index] == 1:
                self.end = Node((x, height - 1))
                self.end.add_connection(top_nodes[x])
                self.nodes.add(self.end)
                break

        # Set distance to end for all nodes
        for n in self.nodes:
            n.set_distance_to_end(self.end)
        self.end.distance_to_end = 0

