#!/usr/bin/python2.7

#############################################################
#								::ROUTING SOFTWARE::
#
#	Desc: 
#	Author:
# 	Date:
#
#############################################################

GLOBAL_DEBUG = True

####################
#		  IMPORTS		 	#
####################

import socket
import time
import os
import threading
from Queue import Queue as queue
from Queue import Empty
from Queue import Full


####################
#		  CONSTANTS		 #
####################

UDP_IP                 	= "127.0.0.1"
PACMAN_PORT          = 2000
GHOST_PORT            = 3000
STATS_PORT              = 4000
AI_PORT                     = 5000
GUI_PORT           	 = 6000
PIXYIO_PORT      	 = 7000

RVR_ACK                 = "ACK"
RVR_ACK_TIMEOUT  = 0.30



####################
#		  GLOBALS		 #
####################
globalThreadingLock = threading.Lock()




####################
#		  FUNCTIONS		 #
####################

def clearScreen():
	os.system('cls' if os.name == 'nt' else 'clear')
	
	
def dbgPrint(dtype, msg):
	if GLOBAL_DEBUG is True:
		globalThreadingLock.acquire()
		print("- " + dtype + ": " + msg)
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
		
			dbgPrint("SOCK", "Opened socket %s:%i" % (IP, PORT))
			
			return sock
		except IOError as e:
			if retry is 5:
				print(e)
				exit(0)
			else:
				retry += 1


####################
#		 IO OBJECTS		 #
####################            
     
class RVRIOObject:
        def __init__(self, IP, PORT, rvrID):
        
        	dbgPrint("INIT", "RVRIOObject ID: " + rvrID)
        
                self._sendAddress = (IP, PORT)
                self._rxSock = openUDPSocket(IP, PORT, "READ")
                self._txSock = openUDPSocket(IP, PORT+1, "WRITE")
                
                self._txQ = queue()
                self._rxQ = queue()
                
                self._rvrID = rvrID
                
                self.run()
                
        def write(self, data):
                self._txQ.put(data, block=True)
                
        def read(self):
                try:
                        data = self._rxQ.get(block=False)
                except Empty:
                        pass
                else:
                        return data

        def ioWriteWorker(self):
        	
        	dbgPrint("THREAD START", "ioWriteWorker() in RVRIOObject ID: %s" % self._rvrID)
        	
                while True:
                        
                        txData = self._txQ.get(block=True)
                        self._txSock.sendto(txData, self._sendAddress)
                   
                        writeTime = time.time() * 1000                
                        
                        while True:
                        
                                rxData = self._rxSock.recv(65536)
                                readTime = time.time()
                                
                                if rxData is not RVR_ACK:
                                        self._rxQ.put(rxData, block = True)
                                elif rxData is RVR_ACK and (readTime - writeTime) <= RVR_ACK_TIMEOUT:
                                        break
                                if (readTime - writeTime) > RVR_ACK_TIMEOUT:
                                        self._txSock.sendto(txData, self._sendAddress)
                                        writeTime = time.time()
                                        
                                        dbgPrint("WARN", "%s took longer than %i to ACK!" % (self._rvrID, RVR_ACK_TIMEOUT))
                              
        def ioReadWorker(self):
                
                dbgPrint("THREAD START", "ioReadWorker() in RVRIOObject ID: %s" % self._rvrID)
                
                while True:
                        
                        rxData = self._rxSock.recv(65536)
                        
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
		self._sendAddress = (IP, PORT)
		
		dbgPrint("INIT", "ioObject ID: " + ID)
		
		self._rxSock = openUDPSocket(IP, PORT, "READ")
		self._txSock = openUDPSocket(IP, PORT+1, "WRITE")
		
		self._txQ = queue()
		self._rxQ = queue()
		
		self._ID = ID
		
		self.run()
		
	def write(self, data):
		self._txQ.put(data, block=True)
		
	def read(self):
                try:
                        data = self._rxQ.get(block=False)
                except Empty:
                        pass
                else:
                        return data
                        
        def ioWriteWorker(self):
        	
        	dbgPrint("THREAD START", "ioWriteWorker() in ioObject ID: %s" % self._ID)
        	
        	while True:
        		txData = self._txQ.get(block=True)
        		self._txSock.sendto(self._sendAddress)
        
        def ioReadWorker(self):
        
        	dbgPrint("THREAD START", "ioReadWorker() in ioObject ID: %s" % self._ID)
        	
        	while True:
        	
        		rxData = self._rxSock.recv(65536)
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
#	    	  			        MAIN		 		           #
#######################################

if __name__ == "__main__":

	# Welcome message
	clearScreen()
	print("[ ROUTING START ]\n")

        # Create IO objects
        PACMAN = RVRIOObject(UDP_IP, PACMAN_PORT, "PACMAN")
        GHOST = RVRIOObject(UDP_IP, GHOST_PORT, "GHOST")
        GUI = ioObject(UDP_IP, GUI_PORT, "GUI")
        AI = ioObject(UDP_IP, AI_PORT, "AI")
        STATS = ioObject(UDP_IP, STATS_PORT, "STATS")
	
	#
	
	
