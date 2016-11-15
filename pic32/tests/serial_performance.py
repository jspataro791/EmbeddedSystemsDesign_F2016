# This script sends repetitive data over a USB port serially
# It monitors how long it takes microcontroller to ACK
# Prints statistics

import serial
import time
import sys
import os

args = sys.argv

# Consts
TIMEOUT_THRESHOLD = 0.3
READLINE_TIMEOUT = 0.01
OUTPUT_SLEEP_TIME = 0.1
UC_ACK = "ACK"
DBG_MSG_REFRESH = 10
DBG_MSG_NUM_ROLLOVER = 127
MSG_NUM_BYTES = 4

# Clearscreen
def clearScreen():
	os.system('cls' if os.name == 'nt' else 'clear')


# Setup Serial 

try:
	ser = serial.Serial(
		port = args[1],
		baudrate = 115200,
		parity = serial.PARITY_NONE,
		stopbits = serial.STOPBITS_ONE,
		bytesize = serial.EIGHTBITS,
		timeout = READLINE_TIMEOUT
	)

	ser.close()

	ser.open()

except serial.SerialException as e:
	print(e.strerror)
	exit(0)

# Data frames
validData				= "\xFE\x00\x01\x02\x03\xFF"
invalidDataOverflow 	= "\xFE\x00\x01\x02\x03\x04\x05\x06\x07\x08\x09\x10\x11\x12\xFF"
invalidDataUnderflow	= "\xFE\x00\x01\x02xFF"
invalidDataDoubleStart	= "\xFE\xFE\x00\x01\x02\x03\xFF"
invalidDataDoubleStop	= "\xFE\x00\x01\x02\x03\xFF\xFF"
invalidDataNoStart		= "\x00\x01\x02\x03\xFF"
invalidDataNoStop		= "\xFE\x00\x01\x02\x03"



# Pick data out

dataOut = ""
dataType = ""

if len(args) < 3:
	dataOut = validData
	dataType = "VALID"
else:
	
	dataType = args[2][1:]
	
	if args[2] == "-VALID":
		dataOut = validData
	elif args[2] == "-OVERFLOW":
		dataOut = invalidDataOverflow
	elif args[2] == "-UNDERFLOW":
		dataOut = invalidDataUnderflow
	elif args[2] == "-DOUBLESTART":
		dataOut = invalidDataDoubleStart
	elif args[2] == "-DOUBLESTOP":
		dataOut = invalidDataDoubleStop
	elif args[2] == "-NOSTART":
		dataOut = invalidDataNoStart
	elif args[2] == "-NOSTOP":
		dataOut = invalidDataNoStop
	else:
		dataOut = validData
		dataType = "VALID"
	

# Counts
goodCount = 0
badCount = 0

timeStart = time.time()

writeTime = 0
readTime = 0
ackTimes = []
average = 0

dbgrcvd = 0
dbgmsgs = []
dbglost = 0
dbgfirst = 1

ser.flush()

while(1):
	""" clear the screen """
	clearScreen()
	
	""" PRINT STATISTICS """
	print("[TXRATE = %f SEC, TIMEOUT = %f SEC]\n[DATA = %s, MSGBYTES = %i, ACK = '%s']\n[%s]\n--------------------------------------------"
																 % (OUTPUT_SLEEP_TIME,TIMEOUT_THRESHOLD, dataType
																	,MSG_NUM_BYTES, UC_ACK,repr(dataOut)))
	sys.stdout.write("SEC: %i, QUICK ACK: %i, NO ACK: %i" % (
				time.time() - timeStart,goodCount,badCount)) 
	sys.stdout.write("\nAVG ACKTIME: %i MS, ACK RATIO: %i%%\n" % (average, 
			(float(badCount)/float(goodCount))*100 if goodCount != 0 else 0))
	sys.stdout.write("DBG RCVD: %i, DBG LOST: %i, DBG RATIO: %i%%\n--------------------------------------------\n" 
												% (dbgrcvd, dbglost, 
												(float(dbglost)/float(dbgrcvd))*100 if dbgrcvd != 0 else 0))
	
	""" print the debug response messages """
	for i in range(len(dbgmsgs)):
		#print(' ' * 50 + "\r"),
		print(dbgmsgs[i])
	
	sys.stdout.flush() 

	""" wait between sending messages """
	time.sleep(OUTPUT_SLEEP_TIME)
	
	""" set up time stat """
	#sys.stdout.write("\r")
	writeTime = time.time() * 1000

	""" write out data to serial """
	ser.write(dataOut)
	ser.flush()

	timeCount = 0
	
	""" Wait for response loop """
	while(1): 
		""" get bytes from serial """
		response = ser.read(MSG_NUM_BYTES)
		
		try:
			""" if we get a debug message..."""
			if response[0:1].find("\xFE") != -1:

				""" this refreshes the debug message queue so we don't overflow the screen """
				if len(dbgmsgs) > DBG_MSG_REFRESH:
					dbgmsgs = []

				""" this places the debug message on the debug message queue """
				dbgmsgs.append(	"RCV: %s ---> %c%i\r" % 
							(repr(response), str(response[1]), ord(response[MSG_NUM_BYTES - 2]) ))

				""" calculate the number of missed messages, accounting for rollover """
				if dbgfirst == 0:

					if ord(response[MSG_NUM_BYTES - 2]) > dbglast:

						diff = (ord(response[MSG_NUM_BYTES - 2]) - dbglast)

						if diff < 0:
							dbglost += diff + DBG_MSG_NUM_ROLLOVER
						else:
							dbglost += diff - 1
			
							
				else:
					dbglost = 0
	
				""" sets the last debug message (used for finding missing ones) """
				dbglast = ord(response[MSG_NUM_BYTES - 2])

				dbgrcvd += 1
				dbgfirst = 0
		except IndexError:
			dbgmsgs.append("ERR: Could not read RCV message.\r")
			dbglost += 1
			pass

		""" if we read an acknowledge from serial """
		if response[0:3] == UC_ACK:
			goodCount += 1
			readTime = time.time() * 1000
			ackTimes.append(readTime - writeTime)
			average = sum(ackTimes)/len(ackTimes)
		
			break

		else:
			timeCount += READLINE_TIMEOUT
		
			if timeCount > TIMEOUT_THRESHOLD:
				badCount += 1
				#print("Waited longer than %f for ACK" % TIMEOUT_THRESHOLD)
				break

	


