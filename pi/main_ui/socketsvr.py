import socket
from Queue import Queue as queue
from Queue import Empty, Full
import threading
import time

RX_BREAK_CHAR = '|'
RX_ACK_MSG = "ACK"

TX_START_SEQ = "\xFE\xFE\xFE"
TX_END_SEQ = "\xFF\xFF"
TX_SPD_CHAR = "S"
TX_DIR_CHAR = "D"
TX_DBG_CHAR = "G"
TX_END_CHAR = "E"
TX_MSG_LENGTH = "\x07"

class RoverSocketServer():
    
    def __init__(self, ip, socket, id, acktimeout=2):
        
        # members
        self._ip = ip
        self._socket = socket
        self._id = id
        self._acktimeout = acktimeout
        self._txQ = queue()
        self._rxQ = queue()
        self._ACKQ = queue()
        

        
        # open socket
        self._tcpSock = self._openTCPSocket()
        
        # run
        self.run()
        
        
    def _openTCPSocket(self):
  
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self._ip, self._socket))
            
        except IOError as e:
            print("Could not open TCP socket for %s" % self._id)
                        
        return s
    
    def write(self, data):
        self._txQ.put(data, block=True)
                
    def read(self):
        try:
            data = self._rxQ.get(block=False)
        except Empty:
            return None
        else:
            return data

    def _ioWriteWorker(self):
            
        print("THREAD START", "ioWriteWorker() in RoverSocketServer ID: %s" % self._id)
        
        while True:
                
            try:
                txData = self._txQ.get(block=True)
                self._tcpSock.send(txData)

                print("IO", "ioWriteWorker() in RoverSocketServer ID: %s sent %s" % (self._id, txData.encode('hex')))
                
                print("INFO", "ioWriteWorker() in RoverSocketServer ID: %s waiting for ACK..." % self._id)

                while True:
                        
                    try:
                        self._ACKQ.get(block=True, timeout=self._acktimeout)

                        print("INFO", "ioWriteWorker() in RoverSocketServer ID: %s received ACK!" % self._id)

                        break

                    except Empty:
                        print("WARN", "ioWriteWorker() in RoverSocketServer ID: %s waited for ACK longer than %2f seconds!"
                                % (self._id, self._acktimeout))
                        self._tcpSock.send(txData)      
                       
            except IOError as e:
                    pass
                          
    def _ioReadWorker(self):
            
        print("THREAD START", "ioReadWorker() in RoverSocketServer ID: %s" % self._id)
        
        rxBuf = ""
        
        while True:
                
            rxData = self._tcpSock.recv(1)
            
            if rxData == RX_BREAK_CHAR:
                if rxBuf == RX_ACK_MSG:
                    self._ACKQ.put("ACK", block=False)
                else:
                    self._txQ.put(rxBuf, block=False)
                rxBuf = ""    
                
            else:
                rxBuf += rxData
            
                    
    def run(self):

        print("INFO", "Starting threads in RoverSocketServer ID: " + self._id)

        ioWriteThread = threading.Thread(target=self._ioWriteWorker)
        ioReadThread = threading.Thread(target=self._ioReadWorker)

        ioWriteThread.setDaemon(True)
        ioReadThread.setDaemon(True)

        ioWriteThread.start()
        ioReadThread.start()
        

class RoverDataObj():
    
    def __init__(self):
        
        self._spd = 0
        self._dir = 0
        self._debug = 1
        
    def setSpeed(self, spd):
        if spd > 16 or spd < 0:
            print("Rover speed must be between 0 and 16")
        else:
            self._spd = spd
    
    def setDir(self, dir):
        if dir == "STRAIGHT":
            self._dir = 0
        if dir == "LEFT":
            self._dir = 1
        if dir == "RIGHT":
            self._dir = 2
        else:
            print("Rover direction cannot be %s" % dir)
        
    def setDbg(self, dbgStat):
        if dbgStat == True:
            self._debug = 1
        if dbgStat == False:
            self._debug = 0
        else:
            print("Rover debug cannot be %s" % dbgStat)
      
        
    def __repr__(self):
        
        return (TX_START_SEQ +  TX_MSG_LENGTH + TX_SPD_CHAR + chr(self._spd) + TX_DIR_CHAR 
                + chr(self._dir) + TX_DBG_CHAR + chr(self._debug) + TX_END_CHAR + TX_END_SEQ)
        
        
        