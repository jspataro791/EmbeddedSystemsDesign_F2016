# NodeView.py
# Very crude QT-based viewer for depicting a NodeList. Could be polished for
# end user, but this was just thrown together for quick debugging.
#
# Created by: Benjamin M. Singleton
# Created: 11-29-2016
# Modified:

from PyQt5 import QtGui, QtCore, QtWidgets
import sys
from parameters import *
from NodeList import *


class NodeCanvas(QtWidgets.QWidget):
    def __init__(self):
        super(NodeCanvas, self).__init__()
        self.nodeList = None
        self.setup()

    def setup(self):
        self.setGeometry(0, 0, HORIZONTAL_PIXELS, VERTICAL_PIXELS)
        self.setWindowTitle('Node List')
        self.show()

    def paintEvent(self, e):
        my_painter = QtGui.QPainter()
        my_painter.begin(self)
        self.draw_nodes(my_painter)
        my_painter.end()

    def draw_nodes(self, my_painter):
        if self.nodeList is None:
            return

        horizontal_nodes = 10
        vertical_nodes = 10

        for y in range(vertical_nodes):
            for x in range(horizontal_nodes):
                my_painter.setPen(QtGui.QColor(0, 0, 0))
                my_painter.drawRect(x * node_width, y * node_height, node_width, node_height)
                try:
                    node = self.nodeList.coordinates['%d, %d' % (x, y)]
                except:
                    continue
                mid_x = (x * node_width) + (node_width / 2)
                mid_y = (y * node_height) + (node_height / 2)
                my_painter.setPen(QtGui.QColor(255, 0, 0))
                if node.neighbors['North'] is not None:
                    # draw top half of a vertical line
                    my_painter.drawLine(mid_x, y * node_height, mid_x, mid_y)
                if node.neighbors['East'] is not None:
                    # draw right half of horizontal line
                    my_painter.drawLine(mid_x, mid_y, (x + 1) * node_width, mid_y)
                if node.neighbors['South'] is not None:
                    # draw bottom half of a vertical line
                    my_painter.drawLine(mid_x, mid_y, mid_x, (y + 1) * node_height)
                if node.neighbors['West'] is not None:
                    # draw left half of horizontal line
                    my_painter.drawLine(x * node_width, mid_y, mid_x, mid_y)

def main():
    app = QtWidgets.QApplication(sys.argv)
    test_canvas = NodeCanvas()

    n = NodeList()
    #n.add_node(0, 0, None, True, None, None)
    #n.add_node(1, 0, None, None, None, True)
    #n.connect_all_nodes()
    #print(n.coordinates['0, 0'].neighbors['East'])
    n.from_file('nodes2.txt')
    test_canvas.nodeList = n

    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
