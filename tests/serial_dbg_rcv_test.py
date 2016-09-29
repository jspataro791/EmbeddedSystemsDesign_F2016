import serial
import time
import sys
import os

args = sys.argv[1]

READLINE_TIMEOUT = 0.2

# Setup Serial 
ser = serial.Serial(
	port = args,
	baudrate = 9600,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	#timeout = READLINE_TIMEOUT
)

ser.close()
ser.open()

while(1):
	response = ser.read(4)

	print("RCV: %s ---> %c%i" % (repr(response), str(response[1]), ord(response[2]) ))
