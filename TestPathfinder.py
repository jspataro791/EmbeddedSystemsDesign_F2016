# Pathfinder_test.py
# Unit tests for AI path-finding algorithm for ECE 4534.
#
# Created by: Benjamin M. Singleton
# Created: 10-10-2016
# Modified: 12-01-2016

import unittest
from Pathfinder import Pathfinder
from NodeList import Node, NodeList


class TestPathfinder(unittest.TestCase):
    """
    Unit tests for the Pathfinder class.
    """
    def setup_pathfinder(self):
        p = Pathfinder()
        n = NodeList()
        n.from_file('nodes.txt')
        p.node_list = n
        return p

    def setup_pathfinder2(self):
        p = Pathfinder()
        n = NodeList()
        n.from_file('nodes2.txt')
        p.node_list = n
        return p

    # test the get_estimated_cost function
    def test_pathfinder_1(self):
        self.assertTrue(Pathfinder.get_estimated_cost(Node(0, 0), Node(0, 0)) < 2)
        #print(Pathfinder.get_estimated_cost(Node(0, 0), Node(0, 1)))
        #print(Pathfinder.get_estimated_cost(Node(0, 0), Node(3, 3)))
        self.assertTrue(Pathfinder.get_estimated_cost(Node(0, 0), Node(0, 1)) < 3)
        self.assertTrue(Pathfinder.get_estimated_cost(Node(0, 0), Node(3, 3)) == 7)

    # test the get_path function
    def test_pathfinder_2(self):
        pass

    # start testing the find_path function
    def test_pathfinder_3(self):
        # test the simplest path
        p = self.setup_pathfinder()
        start_node = p.node_list.coordinates['0, 0']
        destination_node = p.node_list.coordinates['1, 0']
        path = p.find_path(start_node=start_node, previous_node=None, destination_node=destination_node)
        print(len(path))
        for each in path:
            print(each)
        print('\n')
        self.assertTrue(len(path) == 2)
        self.assertTrue(path[0] == start_node)
        self.assertTrue(path[1] == destination_node)

    def test_pathfinder_4(self):
        # test a slightly harder path
        p = self.setup_pathfinder()
        start_node = p.node_list.coordinates['0, 0']
        destination_node = p.node_list.coordinates['2, 0']
        path = p.find_path(start_node=start_node, previous_node=None, destination_node=destination_node)
        self.assertTrue(len(path) == 3)
        self.assertTrue(path[0] == start_node)
        self.assertTrue(path[1].x == 1 and path[1].y == 0)
        self.assertTrue(path[2] == destination_node)


    def test_pathfinder_5(self):
        # test a harder path
        p = self.setup_pathfinder()
        start_node = p.node_list.coordinates['0, 0']
        destination_node = p.node_list.coordinates['1, 3']
        path = p.find_path(start_node=start_node, previous_node=None, destination_node=destination_node)
        for each in path:
            print(str(each))
        self.assertTrue(len(path) == 5)
        self.assertTrue(path[0] == start_node)
        #self.assertTrue(path[1].x == 1 and path[1].y == 0) # could go either way
        self.assertTrue(path[2].x == 1 and path[2].y == 1)
        self.assertTrue(path[3].x == 1 and path[3].y == 2)
        self.assertTrue(path[4] == destination_node)

    def test_pathfinder_6(self):
        p = self.setup_pathfinder2()
        start_node = p.node_list.coordinates['2, 3']
        destination_node = p.node_list.coordinates['4, 0']
        path = p.find_path(start_node=start_node, previous_node=None, destination_node=destination_node)
        for each in path:
            print(each)

    def test_pathfinder_7(self):
        p = self.setup_pathfinder2()
        start_node = p.node_list.coordinates['2, 3']
        destination_node = p.node_list.coordinates['4, 0']
        path = p.bfs(start_node=start_node, previous_node=None, destination_node=destination_node)
        for each in path:
            print(each)

if __name__ == '__main__':
    unittest.main()
