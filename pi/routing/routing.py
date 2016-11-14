#!/usr/bin/python2.7

#############################################################
#                   ::ROUTING SOFTWARE::                    #
#                                                           #
#    Desc: Software used to route data between processes on #
#          the Raspberry Pi and the Rovers                  #
#    Author: John Spataro                                   #
#    Date: 10/12/2016                                       #
#                                                           #
#############################################################

GLOBAL_DEBUG = True

####################
#      IMPORTS     #
####################

import socket
import time
import os
import threading
import datetime
from datetime import datetime as dt
import ConfigParser
from Queue import Queue as queue
from Queue import Empty
from Queue import Full


####################
#    CONSTANTS     #
####################

CONFIG_FILE_PATH                = "../common/conf/ports.conf"
LOG_FILE_PATH                   = "../common/log/routing.log"

UDP_IP                          = "127.0.0.1"
PACMAN_PORT                     = 2000
GHOST_PORT                      = 3000
STATS_PORT                      = 4000
AI_PORT                         = 5000
GUI_PORT                        = 6000
PIXYIO_PORT                     = 7000

RVR_START_BYTE                  = "\xFE"
RVR_STOP_BYTE                   = "\xFF"
RVR_ACK                         = "ACK"
RVR_ACK_TIMEOUT                 = 5
RVR_FRUIT                       = "FRUIT!"

GHOST_RVR_CUR_SPEED             = 5
PACMAN_RVR_CUR_SPEED            = 16

GUI_LEFT                        = "LEFT"
GUI_RIGHT                       = "RIGHT"

AI_LEFT                         = "LEFT"
AI_RIGHT                        = "RIGHT"



####################
#     MUTEXES      #
####################
globalThreadingLock = threading.Lock()


####################
#     FILE I/O     #
####################
logfile = open(LOG_FILE_PATH, "w")


####################
#    FUNCTIONS     #
####################

def clearScreen():
        os.system('cls' if os.name == 'nt' else 'clear')
        
        
def dbgPrint(dtype, msg):
        if GLOBAL_DEBUG is True:
                
                curTime = dt.now().strftime('%H:%M:%S.%f')
                
                globalThreadingLock.acquire()
                print(curTime + " - " + dtype + ": " + msg)
                global logfile
                logfile.write( curTime + ", " + 
                                dtype + ": " + msg + "\n")
                globalThreadingLock.release()
                
                
def openUDPSocket(IP, PORT, IO_INTENT):

        retry = 1

        while(1):
                try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        sock.setblocking(1)

                        if IO_INTENT is "READ":
                                sock.bind((IP, PORT))
                        elif IO_INTENT is "WRITE":
                                sock.connect((IP, PORT))
                        else:
                                raise IOError("Invalid IO intent for %s:%i" % (IP,PORT))
                
                        dbgPrint("SOCK", "Opened socket %s:%i in mode %s" % (IP, PORT, IO_INTENT))
                        
                        return sock
                except IOError as e:
                        if retry is 5:
                                print(e)
                                exit(0)
                        else:
                                retry += 1


def fillRVRDatagram(speed, direction):
        spd = "S" + chr(speed)
        binDirection = 0
        if direction == "LEFT":
                binDirection = 0
        elif direction == "RIGHT":
                binDirection = 1

        direc = "D" + chr(binDirection)

        dataTotal = spd + direc
        
        numBytesOfData = chr(len(dataTotal))
        
        return RVR_START_BYTE + numBytesOfData + dataTotal + RVR_STOP_BYTE




####################
#   IO OBJECTS     #
####################            
     
class RVRIOObject:
        def __init__(self, IP, PORT, rvrID):
        
                dbgPrint("INIT", "RVRIOObject ID: " + rvrID)
        
                self._sendAddress = (IP, PORT+1)
                self._dpSock = openUDPSocket(IP, PORT, "READ")
                                
                self._txQ = queue()
                self._rxQ = queue()

                self._ACKQ = queue()
                
                self._rvrID = rvrID
                
                self.run()
                
        def write(self, data):
                self._txQ.put(data, block=True)
                
        def read(self):
                try:
                        data = self._rxQ.get(block=True)
                except Empty:
                        pass
                else:
                        return data

        def ioWriteWorker(self):
                
                dbgPrint("THREAD START", "ioWriteWorker() in RVRIOObject ID: %s" % self._rvrID)
                
                while True:
                        
                        try:
                                txData = self._txQ.get(block=True)
                                self._dpSock.sendto(txData, self._sendAddress)


                                dbgPrint("IO", "ioWriteWorker() in RVRIOObject ID: %s sent %s" % (self._rvrID, txData.encode('hex')))
                                
                                dbgPrint("INFO", "ioWriteWorker() in RVRIOObject ID: %s waiting for ACK..." % self._rvrID)

                                while True:
                                        
                                        try:
                                                self._ACKQ.get(block=True, timeout=RVR_ACK_TIMEOUT)

                                                dbgPrint("INFO", "ioWriteWorker() in RVRIOObject ID: %s received ACK!" % self._rvrID)

                                                break

                                        except Empty:
                                                dbgPrint("WARN", "ioWriteWorker() in RVRIOObject ID: %s waited for ACK longer than %2f seconds!"
                                                                                                        % (self._rvrID, RVR_ACK_TIMEOUT))
                                                self._dpSock.sendto(txData, self._sendAddress)      
                                   
                        except IOError as e:
                                pass
                              
        def ioReadWorker(self):
                
                dbgPrint("THREAD START", "ioReadWorker() in RVRIOObject ID: %s" % self._rvrID)
                
                while True:
                        
                        rxData = self._dpSock.recv(65536)

                        if rxData == RVR_ACK:
                                self._ACKQ.put("ACK", block=True)
                        else:
                                self._rxQ.put(rxData, block=True)
                        
        def run(self):

                dbgPrint("INFO", "Starting threads in RVRIOObject ID: " + self._rvrID)

                ioWriteThread = threading.Thread(target=self.ioWriteWorker)
                ioReadThread = threading.Thread(target=self.ioReadWorker)

                ioWriteThread.setDaemon(True)
                ioReadThread.setDaemon(True)

                ioWriteThread.start()
                ioReadThread.start()
                        
                
class ioObject:
        def __init__(self, IP, PORT, ID):
                self._sendAddress = (IP, PORT+1)
                
                dbgPrint("INIT", "ioObject ID: " + ID)
                
                self._dpSock = openUDPSocket(IP, PORT, "READ")
                
                self._txQ = queue()
                self._rxQ = queue()
                
                self._ID = ID
                
                self.run()
                
        def write(self, data):
                self._txQ.put(data, block=True)
                
        def read(self):
                try:
                        data = self._rxQ.get(block=True)
                except Empty:
                        pass
                else:
                        return data
                        
        def ioWriteWorker(self):
                
                dbgPrint("THREAD START", "ioWriteWorker() in ioObject ID: %s" % self._ID)
                
                while True:
                        txData = self._txQ.get(block=True)
                        self._dpSock.sendto(txData, self._sendAddress)

                        dbgPrint("IO", "ioWriteWorker() in ioObject ID: %s sent %s" % (self._ID, txData))
        
        def ioReadWorker(self):
        
                dbgPrint("THREAD START", "ioReadWorker() in ioObject ID: %s" % self._ID)
                
                while True:
                
                        rxData = self._dpSock.recv(65536)
                        self._rxQ.put(rxData, block=True)
                        
                        
        def run(self):
                                    
                dbgPrint("INFO", "Starting threads in ioObject ID: " + self._ID)
                
                ioWriteThread = threading.Thread(target=self.ioWriteWorker)
                ioReadThread = threading.Thread(target=self.ioReadWorker)
                
                ioWriteThread.setDaemon(True)
                ioReadThread.setDaemon(True)
                
                ioWriteThread.start()
                ioReadThread.start()
                

                
                
#######################################
#                MAIN                 #
#######################################

if __name__ == "__main__":

        # Welcome message
        clearScreen()
        print("[ ROUTING START ]\n")
        
        # Do config parsing
        
        cparse = ConfigParser.ConfigParser()
        cparse.read(CONFIG_FILE_PATH)
        
        UDP_IP = cparse.get('IOPORTS', 'UDP_IP')
        PACMAN_PORT = cparse.getint('IOPORTS', 'PACMAN_PORT')
        GHOST_PORT = cparse.getint('IOPORTS', 'GHOST_PORT')
        AI_PORT = cparse.getint('IOPORTS', 'AI_PORT')
        GUI_PORT = cparse.getint('IOPORTS', 'GUI_PORT')
        STATS_PORT = cparse.getint('IOPORTS', 'STATS_PORT')
        PIXYIO_PORT = cparse.getint('IOPORTS', 'PIXYIO_PORT')
        
        # Create IO objects
        PACMAN = RVRIOObject(UDP_IP, PACMAN_PORT, "PACMAN")
        GHOST = RVRIOObject(UDP_IP, GHOST_PORT, "GHOST")
        GUI = ioObject(UDP_IP, GUI_PORT, "GUI")
        AI = ioObject(UDP_IP, AI_PORT, "AI")
        STATS = ioObject(UDP_IP, STATS_PORT, "STATS")
        

        # Define handler threads
                # PACMAN HANDLER WORKER
        def PACMANHandlerWorker():
        
                dbgPrint("THREAD START", "PACMANHandlerWorker()")
        
                while True:
                        rxData = PACMAN.read()
                        
                        dbgPrint("IO", "PACMANHandlerWorker() read %s" % rxData)
                
                        if rxData == RVR_FRUIT:
                        
                                dbgPrint("IO", "PACMANHandlerWorker() got a fruit!")
                                
                                GUI.write("FRUIT")
                                AI.write("FRUIT")
                                STATS.write("FRUIT")
                                
                        if rxData.find('D') == 2:
								
                                dbgPrint("IO", "PACMANHandlerWorker() got debug message #%i" 
                                                                                % ord(rxData[3]))
                                
                                STATS.write("&P:" + rxData[2:rxData.find(RVR_STOP_BYTE)])
								                              
                        

                # GHOST HANDLER WORKER        
        def GHOSTHandlerWorker():
                
                dbgPrint("THREAD START", "GHOSTHandlerWorker()")
                
                while True:

                        rxData = GHOST.read()
                        
                        dbgPrint("IO", "GHOSTHandlerWorker() read %s" % rxData)
                        
                        if rxData.find('D') == 2:
								
                                dbgPrint("IO", "GHOSTHandlerWorker() got debug message #%i" 
                                                                                % ord(rxData[3]))
                                
                                STATS.write("&G:" + rxData[2:rxData.find(RVR_STOP_BYTE)])


                # GUI HANDLER WORKER
        def GUIHandlerWorker():
                
                dbgPrint("THREAD START", "GUIHandlerWorker()")

                while True:

                        rxData = GUI.read()

                        dbgPrint("IO", "GUIHandlerWorker() read %s" % rxData)
                
                        if rxData == GUI_LEFT:
                                pacData = fillRVRDatagram(PACMAN_RVR_CUR_SPEED, "LEFT")
                                STATS.write("&P:LEFT")
                                PACMAN.write(pacData)
                        elif rxData == GUI_RIGHT:
                                pacData = fillRVRDatagram(PACMAN_RVR_CUR_SPEED, "RIGHT")
                                STATS.write("&P:RIGHT")
                                PACMAN.write(pacData)
                        else:
                                pass
                
                # AI HANDLER WORKER
        def AIHandlerWorker():
                
                dbgPrint("THREAD START", "AIHandlerWorker()")

                while True:
                
                        rxData = AI.read()
                        
                        dbgPrint("IO", "AIHandlerWorker() read %s" % rxData)

                        if rxData == AI_LEFT:
                                ghostData = fillRVRDatagram(GHOST_RVR_CUR_SPEED, "LEFT")
                                STATS.write("&G:LEFT")
                                GHOST.write(ghostData)
                        elif rxData == AI_RIGHT:
                                ghostData = fillRVRDatagram(GHOST_RVR_CUR_SPEED, "RIGHT")
                                STATS.write("&G:RIGHT")
                                GHOST.write(ghostData)
                        else:
                                pass
        

        # Start handle threads
        
                #PACMAN
        PACMANHandlerThread = threading.Thread(target=PACMANHandlerWorker)
        PACMANHandlerThread.setDaemon(True)
        PACMANHandlerThread.start()
        
                #GHOST
        GHOSTHandlerThread = threading.Thread(target=GHOSTHandlerWorker)
        GHOSTHandlerThread.setDaemon(True)
        GHOSTHandlerThread.start()
                
                #GUI
        GUIHandlerThread = threading.Thread(target=GUIHandlerWorker)
        GUIHandlerThread.setDaemon(True)
        GUIHandlerThread.start()
                
                #AI
        AIHandlerThread = threading.Thread(target=AIHandlerWorker)
        AIHandlerThread.setDaemon(True)
        AIHandlerThread.start()
                
                #STATS
        
        # INPUT LOOP
        while True:
                cmd = raw_input()
                if cmd == "quit" or cmd == "exit":
                        logfile.close()
                        exit(0)
                elif cmd == "clear":
                        clearScreen()
                        

                        
#############################################################
#                    END FILE                               #
#############################################################
