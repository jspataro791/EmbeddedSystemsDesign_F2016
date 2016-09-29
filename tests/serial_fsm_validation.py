import serial
import time
import sys
import os

args = sys.argv[1]

# DATA CONST
DATA_GOOD 		= "\xFE\x01\x02\x03\xFF"
DATA_OVERFLOW 		= "\xFE\x01\x02\x03\x04\xFF"
DATA_UNDERFLOW		= "\xFE\x01\x02\xFF"
DATA_DOUBLE_START	= "\xFE\xFE\x01\x02\x03\xFF"
DATA_DOUBLE_STOP	= "\xFE\x01\x02\x03\xFF\xFF"
DATA_NO_STOP		= "\xFE\x01\x02\x03"
DATA_NO_START		= "\x01\x02\x03\xFF"
DATA_WEIRD_START    = "\xFE\x01\xFE\x02\x03\xFF"


# OTHER CONST
READLINE_TIMEOUT 	= 1
UC_ACK 		 	= "YY"

# Setup Serial 
ser = serial.Serial(
	port = args,
	baudrate = 9600,
	parity = serial.PARITY_NONE,
	stopbits = serial.STOPBITS_ONE,
	bytesize = serial.EIGHTBITS,
	timeout = READLINE_TIMEOUT
)

ser.close()
ser.open()
ser.flush()

# Clearscreen
def clearScreen():
	os.system('cls' if os.name == 'nt' else 'clear')

# Serial check
def serialCheck(msg, data, serial):
	print("\nCHECKING: %s" % msg)

	serial.write(data)
	response = serial.readline()
	print("'%s'" % response),

	if response[0:2] == UC_ACK:
		print("--> ACK")

	else:
		print("--> INVALID")

# SENDS
clearScreen()
print("[SERIAL COMM FSM CHECKER, TIMEOUT = %f SEC]" % READLINE_TIMEOUT)
serialCheck("Good Data", DATA_GOOD, ser)
serialCheck("Overflow Data", DATA_OVERFLOW, ser)
serialCheck("Underflow Data", DATA_UNDERFLOW, ser)
serialCheck("Double Start", DATA_DOUBLE_START, ser)
serialCheck("Double Stop", DATA_DOUBLE_STOP, ser)
serialCheck("No Stop", DATA_NO_STOP, ser)
serialCheck("No Start", DATA_NO_START, ser)
serialCheck("Weird Start Issue", DATA_WEIRD_START, ser)

print("\n[FINISHED]\n")





