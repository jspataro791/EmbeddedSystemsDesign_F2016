# This script sends repetitive data over a USB port serially
# It monitors how long it takes microcontroller to ACK
# Prints statistics

import serial
import time
import sys
import os

# Consts
TIMEOUT_THRESHOLD = 0.1
READLINE_TIMEOUT = 0.01
UC_ACK = "YY"

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


while(1):
	clearScreen()
	print("[SERIAL DATA TEST, TIMEOUT = %f SEC]" % TIMEOUT_THRESHOLD)
	sys.stdout.write("SEC: %i, QUICK ACK: %i, SLOW ACK: %i\r" % (
				time.time() - timeStart,goodCount,badCount)) 
	sys.stdout.flush() 	
		
	ser.write(validData)

	timeCount = 0
	
	while(1): 
		
		
		response = ser.readline()
		
		if response[0:2] == UC_ACK:
			goodCount += 1
			break
		else:
			
			timeCount += READLINE_TIMEOUT

			if timeCount > TIMEOUT_THRESHOLD:
				badCount += 1
				#print("Waited longer than %f for ACK" % TIMEOUT_THRESHOLD)
				break
		
	


