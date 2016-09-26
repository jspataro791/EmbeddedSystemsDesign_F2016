# This script sends repetitive data over a USB port serially

import serial
import time

# Setup Serial 
ser = serial.Serial(
	port = '/dev/ttyUSB0',
	baudrate = 9600,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
)

# Main While
while(1):
	time.sleep(0.1); # Wait
	ser.write("This is a test. ") # Serial Write
	

