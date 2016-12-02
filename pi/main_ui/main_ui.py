
#!/usr/bin/python2.7

# # IMPORTS ##
from PyQt4 import Qt as qt
import numpy as np
import serial
import os
import sys
import time
import datetime
import threading
import socketsvr
from PIL.ImageQt import qt_is_installed
from pip.utils.outdated import SELFCHECK_DATE_FMT


MAINWIN_DEF_LOC_X = 300
MAINWIN_DEF_LOC_Y = 300
MAINWIN_DEF_SIZE_X = 640
MAINWIN_DEF_SIZE_Y = 480

BUTTON_HEIGHT = 150

PAC_DATA_OBJ = socketsvr.RoverDataObj()
PAC_IP = "10.0.0.191"
PAC_PORT = 2000
PAC_SOCK_SRV = socketsvr.RoverSocketServer(PAC_IP, PAC_PORT, "PACMAN")

GST_DATA_OBJ = socketsvr.RoverDataObj()
GST_IP = "10.0.0.192"
GST_PORT = 2000
GST_SOCK_SRV = socketsvr.RoverSocketServer(GST_IP, GST_PORT, "GHOST")



class MainApplication():
    
    def __init__(self, argv):
        
        self._app = qt.QApplication(argv, True)
        self._mainwindow = MainWindow()
        self._mainwindow.show()
        
    def run(self):
        
        self._app.exec_()
        
    def stop(self):
        
        self._app.quit()


class MainWindow(qt.QMainWindow):
    
    def __init__(self):
       super(MainWindow, self).__init__()
       
       # setup subwidgets
       self._main = qt.QSplitter(self)
       self._tabbedView = TabbedView(self)
       self._debugConsole = DebugConsole(self)
       
       # setup subwidget layout
       self._main.addWidget(self._tabbedView)
       self._main.addWidget(self._debugConsole)
       self._main.setOrientation(qt.Qt.Vertical)
       
       # setup this main window       
       self.setGeometry(MAINWIN_DEF_LOC_X, MAINWIN_DEF_LOC_Y, MAINWIN_DEF_SIZE_X, MAINWIN_DEF_SIZE_Y)
       self.setWindowTitle("Embedded Main Window")
       self.setCentralWidget(self._main)
       self.showMaximized()

        
        
class DebugConsole(qt.QTextBrowser):
    
    def __init__(self, parent=None):
        super(DebugConsole, self).__init__(parent)
        
        self._maxHeight = parent.geometry().height()
        
        self.resize(qt.QSize(0,0.3 * self._maxHeight))
        
    def addMsgEvent(self, msg):
        
        curTime = datetime.datetime.now().strftime('%H:%M:%S')
        
        self.append("%s - %s" % (curTime, msg))
        
       
class TabbedView(qt.QTabWidget):
    
    def __init__(self, parent=None):
        super(TabbedView, self).__init__(parent)
                        
        self._ctrl = TabControl(self)
        self._dbg = TabDebug(self)
        self._node = TabNodeView(self)
        
        self.addTab(self._ctrl, "PACMAN Control")
        self.addTab(self._dbg, "Debugging")
        self.addTab(self._node, "Node View")
       
       

class TabControl(qt.QWidget):
    
    def __init__(self, parent=None):
        super(TabControl, self).__init__(parent) 
        
        self._mainLayout = qt.QVBoxLayout()
                
        self._controlLayout = qt.QHBoxLayout()
        self._mainLayout.addLayout(self._controlLayout)
        
        self._startLayout = qt.QHBoxLayout()
        self._mainLayout.addLayout(self._startLayout)
        
        self.setLayout(self._mainLayout)
        
        # buttons
        self._straightBtn = qt.QPushButton(qt.QIcon('graphics/straight_arrow.png'), "STRAIGHT", self)
        self._straightBtn.setFixedHeight(BUTTON_HEIGHT)
        
        self._leftBtn = qt.QPushButton(qt.QIcon('graphics/left_arrow.png'), "LEFT", self)
        self._leftBtn.setFixedHeight(BUTTON_HEIGHT)
        
        self._rightBtn = qt.QPushButton(qt.QIcon('graphics/right_arrow.png'), "RIGHT", self)
        self._rightBtn.setFixedHeight(BUTTON_HEIGHT)
        
        self._startBtn = qt.QPushButton(qt.QIcon('graphics/start.png'), "START", self)
        self._startBtn.setFixedHeight(BUTTON_HEIGHT)
        
        self._stopBtn = qt.QPushButton(qt.QIcon('graphics/stop.png'), "STOP", self)
        self._stopBtn.setFixedHeight(BUTTON_HEIGHT)
        
        # button layout
        self._controlLayout.addWidget(self._leftBtn)
        self._controlLayout.addWidget(self._straightBtn)
        self._controlLayout.addWidget(self._rightBtn)
        
        self._startLayout.addStretch(1)
        self._startLayout.addWidget(self._startBtn)
        self._startLayout.addWidget(self._stopBtn)
        self._startLayout.addStretch(1)
        
        # button callbacks
        self._straightBtn.clicked.connect(self.sendStraightSignal)
        self._leftBtn.clicked.connect(self.sendLeftSignal)
        self._rightBtn.clicked.connect(self.sendRightSignal)
        self._startBtn.clicked.connect(self.start)
        self._stopBtn.clicked.connect(self.stop)
        
        # started
        self._started = False
        
        # status
        self._dirStat = "NONE"
        
    def sendLeftSignal(self):
        if self._started and self._dirStat != "LEFT":
            self.util_setButtonColors("LEFT")
            self.window()._debugConsole.addMsgEvent("Left")
            global PAC_DATA_OBJ
            global PAC_SOCK_SRV
            PAC_DATA_OBJ.setDir("LEFT")
            PAC_SOCK_SRV.write(repr(PAC_DATA_OBJ))
        
    def sendRightSignal(self):
        if self._started and self._dirStat != "RIGHT":
            self.util_setButtonColors("RIGHT")
            self.window()._debugConsole.addMsgEvent("Right")
            PAC_DATA_OBJ.setDir("RIGHT")
            PAC_SOCK_SRV.write(repr(PAC_DATA_OBJ))
        
    def sendStraightSignal(self):
        if self._started and self._dirStat != "STRAIGHT":
            self.util_setButtonColors("STRAIGHT")
            self.window()._debugConsole.addMsgEvent("Straight")
            PAC_DATA_OBJ.setDir("STRAIGHT")
            PAC_SOCK_SRV.write(repr(PAC_DATA_OBJ))
        
    def start(self):
        
        if not self._started:
            self.window()._debugConsole.addMsgEvent("STARTING!")
            PAC_DATA_OBJ.setSpeed(16)
            PAC_SOCK_SRV.write(repr(PAC_DATA_OBJ))
            self._started = True
            
    def stop(self):
        
        if self._started:
            self.window()._debugConsole.addMsgEvent("STOPPING!")
            PAC_DATA_OBJ.setSpeed(0)
            PAC_SOCK_SRV.write(repr(PAC_DATA_OBJ))
            self._started = False
            
    def util_setButtonColors(self, dir):
        
        self._straightBtn.setIcon(qt.QIcon('graphics/straight_arrow.png'))
        self._leftBtn.setIcon(qt.QIcon('graphics/left_arrow.png'))
        self._rightBtn.setIcon(qt.QIcon('graphics/right_arrow.png'))
                               
        if dir == "LEFT":
            self._leftBtn.setIcon(qt.QIcon('graphics/left_arrow_g.png'))
            self._dirStat = "LEFT"
        elif dir == "RIGHT":
            self._rightBtn.setIcon(qt.QIcon('graphics/right_arrow_g.png'))
            self._dirStat = "RIGHT"
        elif dir == "STRAIGHT":
            self._straightBtn.setIcon(qt.QIcon('graphics/straight_arrow_g.png'))
            self._dirStat = "STRAIGHT"
        
        
class TabDebug(qt.QWidget):
    
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent) 
        
        # layouts
        self._hLayout = qt.QHBoxLayout()
        self.setLayout(self._hLayout)
        
        self._vLeftLayout = qt.QVBoxLayout()
        self._vRightLayout = qt.QVBoxLayout()
        self._hLayout.addLayout(self._vLeftLayout)
        self._hLayout.addLayout(self._vRightLayout)
        
        # items        
        self._debugState = qt.QCheckBox("Debugging", self)
        self._debugState.stateChanged.connect(self.setDebugging)
        self._vLeftLayout.addWidget(self._debugState)
        
            # pacman
        self._pacDbgSpeed = self.DebugItem(title="Pacman Speed")
        self._vLeftLayout.addWidget(self._pacDbgSpeed)
        
        self._pacDbgDirection = self.DebugItem(title="Pacman Direction")
        self._vLeftLayout.addWidget(self._pacDbgDirection)
        
        self._pacDbgLFAData = self.DebugItem(title="Pacman LFA Data")
        self._vLeftLayout.addWidget(self._pacDbgLFAData)
        
        self._pacDbgMsgCount = self.DebugItem(title="Pacman Dbg Msg Count")
        self._vLeftLayout.addWidget(self._pacDbgMsgCount)
            
            # ghost
        self._vRightLayout.addSpacing(30)
            
        self._gstDbgSpeed = self.DebugItem(title="Ghost Speed")
        self._vRightLayout.addWidget(self._gstDbgSpeed)
        
        self._gstDbgDirection = self.DebugItem(title="Ghost Direction")
        self._vRightLayout.addWidget(self._gstDbgDirection)
        
        self._gstDbgLFAData = self.DebugItem(title="Ghost LFA Data")
        self._vRightLayout.addWidget(self._gstDbgLFAData)
        
        self._gstDbgMsgCount = self.DebugItem(title="Ghost Dbg Msg Count")
        self._vRightLayout.addWidget(self._gstDbgMsgCount)
        
        
        # update timers
        UpdTimer = qt.QTimer(self)
        UpdTimer.setInterval(300)
        UpdTimer.setSingleShot(False)
        UpdTimer.timeout.connect(self.updPacData)
        UpdTimer.timeout.connect(self.updGstData)
        UpdTimer.start()
        
        
    def updPacData(self):
        global PAC_SOCK_SRV
        rxData = PAC_SOCK_SRV.read()
        
        if rxData == None:
            return
        else:
            pass
        
    def updGstData(self):
        global GST_SOCK_SRV
        rxData = GST_SOCK_SRV.read()
        
        if rxData == None:
            return
        else:
            pass


    def setDebugging(self):
        
        global GST_DATA_OBJ
        global PAC_DATA_OBJ
        global GST_SOCK_SRV
        global PAC_SOCK_SRV
        
        chkd = self._debugState.isChecked()
        
        if chkd:
            self.window()._debugConsole.addMsgEvent("Debugging Enabled")
            GST_DATA_OBJ.setDbg(True)
            PAC_DATA_OBJ.setDbg(True)
            GST_SOCK_SRV.write(repr(GST_DATA_OBJ))
            PAC_SOCK_SRV.write(repr(PAC_DATA_OBJ))      
            
        else:
            self.window()._debugConsole.addMsgEvent("Debugging Disabled")
            GST_DATA_OBJ.setDbg(False)
            PAC_DATA_OBJ.setDbg(False)
            GST_SOCK_SRV.write(repr(GST_DATA_OBJ))
            PAC_SOCK_SRV.write(repr(PAC_DATA_OBJ))   
       
     

    class DebugItem(qt.QGroupBox):
        
        def __init__(self, parent=None, title=""):
            super(self.__class__, self).__init__(title,parent)
            
            self._layout = qt.QVBoxLayout()
            self._layout.setAlignment(qt.Qt.AlignTop)
            self.setLayout(self._layout)
            
            self._line = qt.QLineEdit()
            self._line.setFixedWidth(100)
            self._line.setAlignment(qt.Qt.AlignTop)
            self._line.setReadOnly(True)
            self._layout.addWidget(self._line)
            
        def write(self, msg):
            
            self._line.clear()
            self._line.append(msg)
        
        
class TabNodeView(qt.QWidget):
    
    def __init__(self, parent=None):
        super(self.__class__, self).__init__(parent)
        
        

        
       
if __name__ == "__main__":
    
    app = MainApplication(sys.argv)
    app.run() 
