# Pathfinder.py
# AI path-finding algorithm for ECE 4534.
#
# Created by: Benjamin M. Singleton
# Created: 10-10-2016
# Modified: 12-04-2016
from NodeList import Node, NodeList
import math
import socket


FLEE_TIME_DURATION = 5000  # 5000 ms = 1 s
FLEE_ENABLED = False
FLEE_START_TIME = None

nodelist_file = 'nodes.txt'
ui_port = 7668
viewer_port = 3000
host = '127.0.0.1'
default_orientation = 'North'

class Pathfinder(object):
    def __init__(self):
        super(Pathfinder, self).__init__()
        self.node_list = NodeList()
        self.node_list.from_file('nodes.txt')
        self.last_node = None
        self.current_node = None
        self.current_orientation  = 'North'
        self.ui_socket = None
        self.viewer_socket = None
        try:
            self.open_ui_socket()
        except:
            self.ui_socket = None
        try:
            self.open_viewer_socket()
        except:
            self.viewer_socket = None

    def open_ui_socket(self):
        self.ui_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.ui_socket.connect((host, ui_port))

    def open_viewer_socket(self):
        self.viewer_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    @staticmethod
    def get_estimated_cost(start_node, destination_node):
        """
        Estimates the number of moves between start_node and destination_node. To satisfy A* search this can be an
        overestimate, but not an underestimate.
        :param start_node: Starting node.
        :type start_node: Node
        :param destination_node: Destination node.
        :type destination_node: Node
        :return: The estimated cost (distance) between the two.
        :rtype: int
        """
        delta_x = abs(start_node.x - destination_node.x)
        delta_y = abs(start_node.y - destination_node.y)
        if delta_x < delta_y:
            return math.sqrt(2 * delta_x^2) + delta_y - delta_x
        else:
            return math.sqrt(2 * delta_y^2) + delta_x - delta_y

    @staticmethod
    def get_path(destination):
        """
        Given an end node, follows its parent node, then that node's parent node, etc all the way back to the starting
        node, as indicated by a node with no parent, makes a list of this path and reverses it to get the path from
        start to finish.
        :param destination: The node to work backward from; the goal node.
        :type destination: Node
        :return: List of nodes from start to destination.
        :rtype: list
        """
        path = []
        my_node = destination
        path.append(my_node)
        while my_node.parent is not None:
            my_node = my_node.parent
            path.append(my_node)
        path.reverse()
        return path

    def get_relative_path(self, path, start_orientation):
        """
        Given a list of nodes, returns a list of turning directions (straight, left, or
        right).
        :param path: list of nodes.
        :type path: list
        :return: List of turns.
        :rtype: list
        """
        directions = []
        orientation = start_orientation
        for i in range(1, len(path)):
            source = path[i-1]
            destination = path[i]
            direction = self.node_list.get_relative_direction(source, destination, orientation)
            orientation = self.node_list.get_orientation_from_to(source, destination)
            directions.append(direction)
        return directions

    def send_command(self, command):
        if self.ui_socket is None:
            try:
                self.open_ui_socket()
            except:
                return
        if self.ui_socket is None:
            return
        try:
            self.ui_socket.send(command)
        except:
            pass

    def send_locations(self, locations):
        if self.viewer_socket is None:
            try:
                self.open_viewer_socket()
            except:
                return
        if self.viewer_socket is None:
            return
        try:
            self.viewer_socket.sendto(' '.join([str(x) for x in locations]), (host, viewer_port))
        except:
            pass

    def update_locations(self, locations):
        ghost_x = locations[0]
        ghost_y = locations[1]
        user_x = locations[2]
        user_y = locations[3]
        for each in locations:
            if each < 0:
                print('NEGATIVE COORDINATE VALUE!!!')
                raise Exception()
#        if self.current_node is not None:
            # make sure we're not dealing with a weird jitter
#            if self.node_list.get_orientation_from_to(self.current_node, self.node_list.coordinates['%d, %d' % (ghost_x, ghost_y)]) is None:
#                print('New node and old node are not adjacent!')
#                print('Gracefully skipping this update')
#                return
        # update viewer
        self.send_locations([locations[2], locations[3], locations[0], locations[1]])
        # update internal variables if position has changed
        if self.current_node != self.node_list.coordinates['%d, %d' % (ghost_x, ghost_y)]:
            self.last_node = self.current_node
            self.current_node = self.node_list.coordinates['%d, %d' % (ghost_x, ghost_y)]
            # update rover orientation, if this isn't our first move
            if self.last_node is not None:
                self.current_orientation = self.node_list.get_orientation_from_to(self.last_node, self.current_node)
        # get the shortest path to the user rover
        path = self.bfs(self.current_node, self.last_node, self.node_list.coordinates['%d, %d' % (user_x, user_y)])
        if path is None:
            print('Could not find path between (%d, %d) and (%d, %d)' % (ghost_x, ghost_y, user_x, user_y))
            raise Exception()
        # translate the path into actual directions
        relative_path = self.get_relative_path(path, self.current_orientation)
        self.send_command(relative_path[0])

    def captured(self):
        self.ui_socket.send('Captured')
        self.ui_socket.close()
        self.ui_socket = None # to make sure an exception is thrown if any more communication is attempted

    def bfs(self, start_node, previous_node, destination_node):
        #self.current_orientation = self.node_list.get_orientation_from_to(previous_node, start_node)
        queue = []
        queue.append([start_node])
        while queue:
            path = queue.pop(0)
            my_node = path[-1]
            if my_node == destination_node:
                return path
            # get neighbors
            candidates = [x for x in my_node.neighbors.values() if x is not None]
            # remove previous node from neighbors, because we can't turn 180
            if my_node == start_node and previous_node is not None:
                candidates.remove(previous_node)
            # add a branch to explore for each child node
            for each in candidates:
                child_path = list(path)
                child_path.append(each)
                queue.append(child_path)
        return None

    def find_path(self, start_node, previous_node, destination_node):
        """
        Returns a list of nodes to traverse from start_node to destination_node, without immediately going to
        previous_node. Implements a constrained version of A* (A-star) search.
        :param start_node: Starting node.
        :type start_node: Node
        :param previous_node: The node we entered start_node from.
        :type previous_node: None
        :param destination_node: The node we want to reach.
        :type destination_node: Node
        :return: The list of nodes to traverse from start_node to destination_node.
        :rtype: list
        """
        opened = []
        closed = []

        start_node.heuristic_cost = 0
        start_node.f = 0
        start_node.g = 0
        opened.append(start_node)

        while len(opened) > 0:
            minimum_node = None
            minimum_f = None
            for each_candidate in opened:
                if minimum_node is None or minimum_f > each_candidate.f:
                    minimum_node = each_candidate
                    minimum_f = each_candidate.f


            opened.remove(minimum_node)
            closed.append(minimum_node)
            successors = minimum_node.get_neighbors()
            for each_successor in successors:
                if each_successor == destination_node:
                    # found goal
                    each_successor.parent = minimum_node
                    break

                # get h value for successor
                each_successor.heuristic_cost = Pathfinder.get_estimated_cost(each_successor, destination_node)
                # update g value for successor
                each_successor.g = minimum_node.g + 1
                # determine successor's f value
                each_successor.f = each_successor.g + each_successor.heuristic_cost

                # only add to list if it's not in there
                if each_successor not in opened and each_successor not in closed:
                    each_successor.parent = minimum_node
                    opened.append(each_successor)

        if destination_node.parent is None:
            raise Exception('Completed search without finding valid path to destination.')

        return Pathfinder.get_path(destination_node)


def main():
    pass

if __name__ == '__main__':
    main()
