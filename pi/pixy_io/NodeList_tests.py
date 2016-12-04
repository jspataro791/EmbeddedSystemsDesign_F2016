# Pathfinder_test.py
# Unit tests for custom NodeList data structure used in our
# path-finding algorithm for ECE 4534.
#
# Created by: Benjamin M. Singleton
# Created: 10-10-2016
# Modified:

import unittest
from NodeList import Node, NodeList

class TestNodeList(unittest.TestCase):
    """
    Unit tests for the NodeList class.
    """

    # test cases for node class
    def test_node_1(self):
        n1 = Node(0, 0)
        n2 = Node(1, 0)
        n1.neighbors['East'] = n2
        n2.neighbors['West'] = n1
        self.assertTrue(n1.neighbors['East'].neighbors['West'] == n1)
        self.assertTrue(n2.get_neighbors()[0] == n1)
        self.assertTrue(n2.neighbors['East'] is None)
        self.assertTrue(n2.neighbors['North'] is None)
        self.assertTrue(n2.neighbors['South'] is None)

    # test cases for NodeList class
    def setup_nodelist(self):
        n = NodeList()
        n1 = Node(0, 0)
        n1.neighbors['East'] = True
        n1.neighbors['South'] = True
        n2 = Node(1, 0)
        n2.neighbors['East'] = True
        n2.neighbors['West'] = True
        n2.neighbors['South'] = True
        n3 = Node(2, 0)
        n3.neighbors['West'] = True
        n4 = Node(0, 1)
        n4.neighbors['North'] = True
        n4.neighbors['East'] = True
        n5 = Node(1, 1)
        n5.neighbors['North'] = True
        n5.neighbors['South'] = True
        n5.neighbors['West'] = True
        n6 = Node(1, 2)
        n6.neighbors['North'] = True
        n6.neighbors['South'] = True
        n7 = Node(1, 3)
        n7.neighbors['North'] = True
        n.connect_all_nodes()

    def test_nodelist_1(self):
        n = NodeList()
        self.assertTrue(len(n.coordinates) == 0)
        self.assertTrue(len(n.nodes) == 0)
        n = self.setup_nodelist()


if __name__ == '__main__':
    unittest.main()
