
# ROUTING
# Description goes here you lazy ass


# Import
import socket
from threading import Thread
from Queue import Queue as queue


# Custom Lib Import


# Constants
UDP_IP                 = 'localhost'
RVR1_PORT          = 2000
RVR2_PORT          = 3000
STATS_PORT         = 4000
AI_PORT               = 5000
GUI_PORT            = 6000
PIXYIO_PORT        = 7000


# Thread I/O Classes

class ioReadSocketWorker(Thread):
	def __init__(self, socket, ioQueue, threadID):
		super(Thread, self).__init__()
		self._socket = socket
		self._threadID = threadID
		self._ioQueue = ioQueue

		print("INFO: Starting socket read thread %s" % self._threadID)

	def run(self):
		data, addr = self._socket.recvfrom(1024)
		if self._ioQueue.full() is not True:
    			self._ioQueue.put(data, blocking=True, timeout=2)

	def getThreadID(self):
		return self._threadID


class ioWriteSocketWorker(Thread):
	def __init__(self, socket, ioQueue, threadID):
		super(Thread, self).__init__()
		self._socket = socket
		self._threadID = threadID
		self._ioQueue = ioQueue
		
		print("INFO: Starting socket write thread %s" % self._threadID)

	def run(self):

		data = self._ioQueue.get(block=True)

		print(data)
		
		self._socket.sendall(data)
 
	def getThreadID(self):
		return self._threadID


# I/O Object

class ioObject:
	def __init__(self, IP, PORT, IO_INTENT):
		self._IP = IP
		self._PORT = PORT
		self._ID = "%s:%s" % (repr(IP), repr(PORT))
		
		self._mQ = queue()

		try:
			self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
			self._sock.setblocking(0)
			self._sock.bind((self._IP, self._PORT))
		except IOError as e:
			print(e)
			exit
		
		if IO_INTENT is "IO_READ":
			self._ioThread = ioReadSocketWorker(self._sock, self._mQ, self._ID)
		elif IO_INTENT is "IO_WRITE":
			self._ioThread = ioWriteSocketWorker(self._sock, self._mQ, self._ID)
		else:
			raise IOError("ioObject has no I/O intent")
	
		self._ioThread.run()

	def __del__(self):
		self._ioThread.join()
		
	def write(self, data):
		self._mQ.put(data, block=False)

	def read(self):
		return self._mQ.get(block=False)
		
# ------------------------------ MAIN --------------------------------- #

if __name__ == "__main__":
	RVR1_WRITE = ioObject(UDP_IP, RVR1_PORT, "IO_WRITE")
	print("Test")
	RVR1_WRITE.write("Hello!")
	
	
