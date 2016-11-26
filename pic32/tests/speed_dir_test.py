#!/usr/bin/python2.7

import socket
import os
import sys
import time
import random

args = sys.argv

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("10.0.0.191", 2000))
        
START = "\xFE"
STOP = "\xFF"
        
SPD = "S"
DIR = "D"
DBG = "I"        

spd = 0
direc = 0
while(1):
	
	spd += 1
	if spd > 16:
		spd = 0
	direc += 1
	if direc > 2:
	   direc = 0
              
	print("Spd: %i, Dir: %i" % (spd,direc))
	
	send = START + SPD + chr(spd) + DIR + chr(direc) + DBG + "\x01" + STOP
	
	s.send(send)
	
	ack = s.recv(65536).split("|")
	print(ack)
	
	raw_input()
	
	
	#time.sleep(2)
	
# 	if ack == "ACK":
# 	        time.sleep(1)
# 	        
# 	        continue

	  		 