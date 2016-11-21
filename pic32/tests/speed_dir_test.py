#!/usr/bin/python2.7

import serial
import os
import sys
import time
import random

args = sys.argv

# Setup Serial 

try:
	ser = serial.Serial(
		port = args[1],
		baudrate = 115200,
		parity = serial.PARITY_NONE,
		stopbits = serial.STOPBITS_ONE,
		bytesize = serial.EIGHTBITS,
	)

	ser.close()

	ser.open()

except serial.SerialException as e:
	print(e.strerror)
	exit(0)
        
START = "\xFE"
STOP = "\xFF"
        
spd = 0
direc = 0
while(1):
              
      print("Spd: %i, Dir: %i" % (spd,direc))

      send = START + "S" + chr(spd) + "D" + chr(direc) + STOP
      
      ser.write(send)
      ser.flush()
      
      ack = ser.read(4).replace("|","")
      
      if ack == "ACK":
              time.sleep(1)
              spd += 1
              if spd > 16:
                      spd = 0
              direc += 1
              if direc > 2:
                      direc = 0
              continue
