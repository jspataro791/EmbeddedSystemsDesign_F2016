#############################################################
#								::ROUTING SOFTWARE::
#
#	Desc: 
#	Author:
# 	Date:
#
#############################################################


####################
#		  IMPORTS		 	 #
####################

import socket
import time
import os
from threading import Thread
from Queue import Queue as queue
from Queue import Empty
from Queue import Full

####################
#		 LIB IMPORTS		 #
####################


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


####################
#		  FUNCTIONS		 #
####################

def openUDPPort(IP, PORT, IO_INTENT):

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
		
			print("Opened: " + repr(IP) + ":" + repr(PORT))
			
			return sock
		except IOError as e:
			if retry is 5:
				print(e)
				exit(0)
			else:
				retry += 1

def clearScreen():
	os.system('cls' if os.name == 'nt' else 'clear')

####################
#	    THREAD CLASSES		 #
####################

class ioReadSocketWorker(Thread):
	def __init__(self, socket, ioQueue, threadID):
		Thread.__init__(self)
		self._socket = socket
		self._threadID = threadID
		self._ioQueue = ioQueue

		print("Starting socket read thread %s" % self._threadID)

	def run(self):
		data, addr = self._socket.recvfrom(1024)
		if self._ioQueue.full() is not True:
    			self._ioQueue.put(data, block=True, timeout=2)

	def getThreadID(self):
		return self._threadID


class ioWriteSocketWorker(Thread):
	def __init__(self, socket, ioQueue, threadID, address):
		Thread.__init__(self)
		self._socket = socket
		self._threadID = threadID
		self._ioQueue = ioQueue
		self._address = address
		
		print("Starting socket write thread %s" % self._threadID)

	def run(self):
		data = self._ioQueue.get(block=True)
		self._socket.sendto(data, self._address)
 
	def getThreadID(self):
		return self._threadID

class routerWorker(Thread):
	def __init__(self, ioObject, handler, threadID):
		Thread.__init__(self)
		self._ioObject = ioObject
		self._handler = handler
		self._threadID = threadID

		print("Launched router worker thread %s" % self._threadID)

	def run(self):
		data = self._ioObject.read()
		self._handler(data, self._ioObject)
		self.join()
		
	def getThreadID(self):
		return self._threadID

####################
#	    	  OBJECTS		 	 #
####################

class DuplexIOObject:
	def __init__(self, IP, READPORT=0, WRITEPORT=0):
		self._IP = IP
		self._READPORT = READPORT
		self._WRITEPORT = WRITEPORT

		self._RXQ = queue()
		self._TXQ = queue()

		if self._READPORT is not 0:
			self._readSock = openUDPPort(self._IP, self._READPORT, "READ")
			self._rxWorkerThread = ioReadSocketWorker(self._readSock, self._RXQ, 
															repr(self._READPORT))
			self._rxWorkerThread.setDaemon(True)
			self._rxWorkerThread.start()

		if self._WRITEPORT is not 0:
			self._writeSock = openUDPPort(self._IP, self._WRITEPORT, "WRITE")
			address = (self._IP, self._WRITEPORT)
			self._txWorkerThread = ioWriteSocketWorker(self._writeSock, self._TXQ, 
														str(self._WRITEPORT), address)
			self._txWorkerThread.setDaemon(True)
			self._txWorkerThread.start()

	def write(self, data):
		try:
			self._TXQ.put(data, block=True)
		except Full:
			pass

	def read(self):
		try:
			data  = self._RXQ.get(block=True)
		except Empty:
			pass
		else:
			return data
		

#######################################
#	    	  			        MAIN		 		           #
#######################################

if __name__ == "__main__":

	# Welcome message
	clearScreen()
	print("[ ROUTING START ]\n")

	# Create IO objects
	PACMAN 	= DuplexIOObject(UDP_IP, PACMAN_PORT, PACMAN_PORT + 1)
	GHOST	= DuplexIOObject(UDP_IP, GHOST_PORT, GHOST_PORT + 1)
	GUI 		= DuplexIOObject(UDP_IP, GUI_PORT, GUI_PORT + 1)
	AI 		= DuplexIOObject(UDP_IP, AI_PORT, AI_PORT + 1)

	# Launch Routing Threads
	
		
	

	
	
