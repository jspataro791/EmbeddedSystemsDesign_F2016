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

class Printer():
    
    def __init__(self):
        
        self.callback = None
    
    def setCallback(self,callback):
        self.callback = callback    
    
    def put(self, msg):
        
        if self.callback == None:
            return
        else:
            self.callback(msg)
        
PRINT = Printer()

class RoverSocketServer():
    
    def __init__(self, ip, port, id, acktimeout=0.5):
        
        # members
        self._ip = ip
        self._port = port
        self._id = id
        self._acktimeout = acktimeout
        self._ackQ = queue()
                
        # open socket
        self._tcpSock = self._openTCPSocket()
        
        # state 
        self._reconnect_tries = 0
     
    
        
    def _openTCPSocket(self):
  
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self._ip, self._port))
            s.settimeout(0.01)
            
        except IOError as e:
            PRINT.put("Could not open TCP socket for %s" % self._id)
                        
        return s
 
    def reconnect(self):
        
        PRINT.put("Reconnecting %s, try #%i" % (self._id, self._reconnect_tries))
        self._tcpSock.close()
        self._tcpSock = self._openTCPSocket()
   
    def write(self, data):
        
        
        PRINT.put("Sending %s to %s" % (data.encode('hex'), self._id))
        
        try:
            self._tcpSock.send(data)
        except socket.error:
            pass
        
        PRINT.put("Waiting for ACK on %s" % self._id)
        
        self.read()
        
        try:
            ack = self._ackQ.get(block=True, timeout=0.5)
        except Empty:
            
            PRINT.put("Did not receive ACK on %s" % self._id)
            
            if self._reconnect_tries > 2:
                PRINT.put("Could not reconnect, socket might be dead!")
                self._reconnect_tries = 0
                return
            
            self._reconnect_tries += 1 
            self.reconnect()
            self.write(data)
        else:       
            PRINT.put("Received ACK on %s" % self._id)                
        
    def read(self):
        
        try:
            rcv = self._tcpSock.recv(65536)
        except socket.error:
            return None
        except socket.timeout:
            return None
        
        msgs = rcv.split('|')
        msgs.remove('')
        
        msgToRet = []
        
        for msg in msgs:
            if msg == RX_ACK_MSG:
                self._ackQ.put(msg, block=False)
            else:
                msgToRet.append(msg) 
        
        return msgToRet

                    
    

class RoverDataObj():
    
    def __init__(self):
        
        self._spd = 0
        self._dir = 0
        self._debug = 0
        
    def setSpeed(self, spd):
        if spd > 16 or spd < 0:
            PRINT.put("Rover speed must be between 0 and 16")
        else:
            self._spd = spd
    
    def setDir(self, dir):
        if dir == "STRAIGHT":
            self._dir = 0
        elif dir == "LEFT":
            self._dir = 1
        elif dir == "RIGHT":
            self._dir = 2
        else:
            PRINT.put("Rover direction cannot be %s" % dir)
        
    def setDbg(self, dbgStat):
        if dbgStat == True:
            self._debug = 1
        elif dbgStat == False:
            self._debug = 0
        else:
            PRINT.put("Rover debug cannot be %s" % dbgStat)
      
        
    def __repr__(self):
        
        msg = (TX_START_SEQ +  TX_MSG_LENGTH + TX_SPD_CHAR + chr(self._spd) + TX_DIR_CHAR 
                + chr(self._dir) + TX_DBG_CHAR + chr(self._debug) + TX_END_CHAR + TX_END_SEQ)
        return msg
        
        
        