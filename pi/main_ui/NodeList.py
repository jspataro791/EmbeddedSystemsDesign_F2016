# NodeList.py
# Classes for representing an x, y grid-aligned nodal network. All connections
# are right angles, every node has 2-4 neighboring nodes.
#
# Created by: Benjamin M. Singleton
# Created: 10-10-2016
# Modified: 10-18-2016


class Node(object):
    def __init__(self, x=0, y=0, North = None, South = None, East = None, West = None):
        super(Node, self).__init__()
        self.x = x
        self.y = y
        self.f = None
        self.g = None
        self.heuristic_cost = None
        self.parent = None
        self.neighbors = {}
        self.neighbors['North'] = North
        self.neighbors['South'] = South
        self.neighbors['East'] = East
        self.neighbors['West'] = West

    def __str__(self):
        neighbors_string = ''
        for each_key in self.neighbors.keys():
            if self.neighbors[each_key] is not None:
                if len(neighbors_string) > 0:
                    neighbors_string += ', ' + each_key
                else:
                    neighbors_string += each_key
        return ("%d, %d, " % (self.x, self.y)) + neighbors_string



    def get_neighbors(self):
        return [x for x in [y for y in self.neighbors.values()] if x is not None]


class NodeList(object):
    def __init__(self, fixed_x=None, fixed_y=None):
        super(NodeList, self).__init__()
        """if fixed_x is not None and fixed_y is not None:
            self.nodes = []
            for y in range(0, fixed_y):
                self.nodes.append([])
                for x in range(0, fixed_x):
                    self.nodes.append(Node(x, y))
        else:
            self.nodes = []"""
        self.nodes = []
        self.coordinates = {}

    def __str__(self):
        my_string = ''
        for each_node in self.nodes:
            my_string += str(each_node) + '\n'
        return my_string

    def add_node(self, x, y, North=None, East=None, South=None, West=None):
        n = Node(x, y)
        n.neighbors['North'] = North
        n.neighbors['East'] = East
        n.neighbors['South'] = South
        n.neighbors['West'] = West
        self.nodes.append(n)
        self.coordinates['%d, %d' % (x, y)] = n
        #self.connect_all_nodes()

    def connect_all_nodes(self):
        for each in self.nodes:
            for connection in each.neighbors.keys():
                if each.neighbors[connection] != True:
                    continue
                if connection == 'North':
                    each.neighbors[connection] = self.coordinates['%d, %d' % (each.x, each.y - 1)]
                elif connection == 'East':
                    each.neighbors[connection] = self.coordinates['%d, %d' % (each.x + 1, each.y)]
                elif connection == 'South':
                    each.neighbors[connection] = self.coordinates['%d, %d' % (each.x, each.y + 1)]
                elif connection == 'West':
                    each.neighbors[connection] = self.coordinates['%d, %d' % (each.x - 1, each.y)]

    def generate_grid(self, size):
        self.nodes = []
        self.coordinates = {}
        for j in range(size):
            for i in range(size):
                n = Node(i, j)
                if j > 0:
                    n.neighbors['North'] = True
                if j < size-1:
                    n.neighbors['South'] = True
                if i > 0:
                    n.neighbors['West'] = True
                if i < size-1:
                    n.neighbors['East'] = True
                self.coordinates['%d, %d' % (i, j)] = n
                self.nodes.append(n)

    def from_file(self, file):
        with open(file, 'r') as f:
            text = f.readlines()

        for line in text:
            #print('Processing line %s' % line)
            fields = [x.strip() for x in line.split(',')]
            n = Node()
            n.x = int(fields[0])
            n.y = int(fields[1])
            self.coordinates['%d, %d' % (n.x, n.y)] = n
            if 'North' in fields:
                n.neighbors['North'] = True
            if 'East' in fields:
                n.neighbors['East'] = True
            if 'South' in fields:
                n.neighbors['South'] = True
            if 'West' in fields:
                n.neighbors['West'] = True
            self.nodes.append(n)

        self.connect_all_nodes()

    def save_to_file(self, file):
        with open(file, 'w') as f:
            for each_node in self.nodes:
                f.write(str(each_node) + '\n')

    def get_orientation_from_to(self, source, destination):
        """
        Returns the direction that an agent is facing, knowing that they just traveled from source to destination.
        :param source: Starting node.
        :type source: Node
        :param destination: End/current node.
        :type destination: Node
        :return: The cardinal direction the agent is facing (North, East, South, or West).
        :rtype: str
        """
        if destination not in source.get_neighbors():
            return None
        return [x for x in source.neighbors.keys() if source.neighbors[x] == destination][0]

    def get_relative_direction(self, source, destination, orientation):
        """
        Determines which direction the agent has to turn, from its point of view.
        :param source: Starting node.
        :type source: Node
        :param destination: End node.
        :type destination: Node
        :param orientation: The direction the agent is facing when at source.
        :type orientation: str
        :return: 'Straight', 'Left' or 'Right'.
        :rtype: str
        """
        direction = {}
        direction['North'] = {}
        direction['North']['East'] = 'Right'
        direction['North']['West'] = 'Left'
        direction['East'] = {}
        direction['East']['North'] = 'Left'
        direction['East']['South'] = 'Right'
        direction['South'] = {}
        direction['South']['East'] = 'Left'
        direction['South']['West'] = 'Right'
        direction['West'] = {}
        direction['West']['South'] = 'Left'
        direction['West']['North'] = 'Right'
        if type(orientation) != str or orientation not in ['North', 'East', 'South', 'West']:
            return None
        final_orientation = self.get_orientation_from_to(source, destination)
        if orientation == final_orientation:
            return 'Straight'
        else:
            return direction[orientation][final_orientation]


def main():
    my_nodelist = NodeList()
    my_nodelist.from_file('nodes.txt')
    print(my_nodelist)


if __name__ == '__main__':
    main()
