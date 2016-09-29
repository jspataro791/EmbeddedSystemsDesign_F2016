# This script sends repetitive data over a USB port serially
# It monitors how long it takes microcontroller to ACK
# Prints statistics

import serial
import time
import sys
import os

# Consts
TIMEOUT_THRESHOLD = 0.2
READLINE_TIMEOUT = 0.01
UC_ACK = "YY"
AVG_BIAS = 10

# Clearscreen
def clearScreen():
	os.system('cls' if os.name == 'nt' else 'clear')

# Setup Serial 
ser = serial.Serial(
	port = '/dev/ttyUSB0',
	baudrate = 9600,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = READLINE_TIMEOUT
)

ser.close()

ser.open()

# Data frame
validData = "\xFE\x00\x01\x02\xFF"

# Counts
goodCount = 0
badCount = 0

timeStart = time.time()

writeTime = 0
readTime = 0
ackTimes = []
average = 0

while(1):
	clearScreen()
	print("[SERIAL DATA TEST, TIMEOUT = %f SEC]" % TIMEOUT_THRESHOLD)
	sys.stdout.write("SEC: %i, QUICK ACK: %i, NO ACK: %i\r" % (
				time.time() - timeStart,goodCount,badCount)) 
	sys.stdout.write("\nAVG ACKTIME: %i MS, ACK RATIO: %i%%\n" % (average, 
			(float(badCount)/float(goodCount))*100 if goodCount != 0 else 0))
	sys.stdout.flush() 	
	writeTime = time.time() * 1000	
	ser.write(validData)

	timeCount = 0
	
	while(1): 
				
		response = ser.readline()
		
		if response[0:2] == UC_ACK:
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
		
	


