#!/usr/bin/python2.7

import threading
import ConfigParser
import socket
import time
import os
import random

import routing

####################
#       GLOBS      #
#################### 

CONFIG_FILE_PATH 				= "ports.conf"
UDP_IP                          = "127.0.0.1"
PACMAN_PORT                     = 2000
GHOST_PORT                      = 3000
STATS_PORT                      = 4000
AI_PORT                         = 5000
GUI_PORT                        = 6000
PIXYIO_PORT                     = 7000

NUMFAILED = 0


####################
#       START      #
#################### 

os.system('cls' if os.name == 'nt' else 'clear')

print( "\n\n############# STARTING ROUTING TEST #################" )

# read in ports config
cparse = ConfigParser.ConfigParser()
cparse.read(CONFIG_FILE_PATH)

UDP_IP = cparse.get('IOPORTS', 'UDP_IP')
PACMAN_PORT = cparse.getint('IOPORTS', 'PACMAN_PORT')
GHOST_PORT = cparse.getint('IOPORTS', 'GHOST_PORT')
AI_PORT = cparse.getint('IOPORTS', 'AI_PORT')
GUI_PORT = cparse.getint('IOPORTS', 'GUI_PORT')
STATS_PORT = cparse.getint('IOPORTS', 'STATS_PORT')
PIXYIO_PORT = cparse.getint('IOPORTS', 'PIXYIO_PORT')

# open sockets for write

print("\n## Opening UDP sockets ##\n (This tests UDP socket open sub in routing.py)\n")

openUDPSocket = routing.openUDPSocket        
                      
                                
outsock = openUDPSocket(UDP_IP, 300, "WRITE")
pacsock = openUDPSocket(UDP_IP, PACMAN_PORT+1, "READ")
ghostsock = openUDPSocket(UDP_IP, GHOST_PORT+1, "READ")
aisock = openUDPSocket(UDP_IP, AI_PORT+1, "READ")
guisock = openUDPSocket(UDP_IP, GUI_PORT+1, "READ")
statssock = openUDPSocket(UDP_IP, STATS_PORT+1, "READ")
pixysock = openUDPSocket(UDP_IP, PIXYIO_PORT+1, "READ")


# Data frame filler test

print("\n# Testing rover data frame filler..")

print ("\nS = 53, D = 44")

print("LEFT, SPEED 5")

dgram = routing.fillRVRDatagram(5, "LEFT")



for x in dgram:
	print(x.encode('hex') + " :"),
	
if dgram.encode('hex') == "fe0453054400ff":
	print("PASS")
else:
	print("FAILED!")
	NUMFAILED += 1
	
print("\nRIGHT, SPEED 7")

dgram = routing.fillRVRDatagram(7, "RIGHT")

for x in dgram:
	print(x.encode('hex') + " :"),
	
if dgram.encode('hex') == "fe0453074401ff":
	print("PASS")
else:
	print("FAILED!")
	NUMFAILED += 1


def RUN_IO_TESTS():
	print ("\n\n# Starting individual I/O test...")

	global NUMFAILED

	# send a turn from GUI
	# left
	print ("\n## GUI I/O ##")
	print ("SEND: sending LEFT from GUI")
	outsock.sendto("LEFT", (UDP_IP, GUI_PORT))
	retData = pacsock.recv(65536)

	if retData[retData.find('D') + 1].encode('hex') == "00":
		print("PASS: Got LEFT on PACMAN output")
		outsock.sendto("ACK", (UDP_IP, PACMAN_PORT))
	else:
		print("FAILED!")
		NUMFAILED += 1
		
	retData = statssock.recv(65536)

	print("RECV: waiting for LEFT on STATS input")
	if retData == "&P:LEFT":
		print("PASS: Got LEFT on STATS input")
	else:
		print("FAILED!")
		NUMFAILED += 1


	# right
	print ("SEND: sending RIGHT from GUI")
	outsock.sendto("RIGHT", (UDP_IP, GUI_PORT))
	retData = pacsock.recv(65536)

	if retData[retData.find('D') + 1].encode('hex') == "01":
		print("PASS: Got RIGHT on PACMAN output")
		outsock.sendto("ACK", (UDP_IP, PACMAN_PORT))
	else:
		print("FAILED!")
		NUMFAILED += 1
		
	retData = statssock.recv(65536)

	print("RECV: waiting for RIGHT on STATS input")
	if retData == "&P:RIGHT":
		print("PASS: Got RIGHT on STATS input")
	else:
		print("FAILED!")
		NUMFAILED += 1
				

		

	# send a turn from AI
	# left
	print ("\n## AI I/O ##")
	print ("SEND: sending LEFT from AI")
	outsock.sendto("LEFT", (UDP_IP, AI_PORT))
	retData = ghostsock.recv(65536)

	if retData[retData.find('D') + 1].encode('hex') == "00":
		print("PASS: Got LEFT on GHOST output")
		outsock.sendto("ACK", (UDP_IP, GHOST_PORT))
	else:
		print("FAILED!")
		NUMFAILED += 1
		
	retData = statssock.recv(65536)
	print("RECV: waiting for LEFT on STATS input")
	if retData == "&G:LEFT":
		print("PASS: Got LEFT on STATS input")
	else:
		print("FAILED!")
		NUMFAILED += 1
		


	# right
	print ("SEND: sending RIGHT from AI")
	outsock.sendto("RIGHT", (UDP_IP, AI_PORT))
	retData = ghostsock.recv(65536)

	if retData[retData.find('D') + 1].encode('hex') == "01":
		print("PASS: Got RIGHT on GHOST output")
		outsock.sendto("ACK", (UDP_IP, GHOST_PORT))
	else:
		print("FAILED!")
		NUMFAILED += 1
		
	retData = statssock.recv(65536)
	print("RECV: waiting for RIGHT on STATS input")
	if retData == "&G:RIGHT":
		print("PASS: Got RIGHT on STATS input")
	else:
		print("FAILED!")
		NUMFAILED += 1



	# send messages from PACMAN
	# fruit
	print ("\n## PACMAN I/O ##")
	print ("SEND: sending FRUIT! from PACMAN")
	outsock.sendto("FRUIT!", (UDP_IP, PACMAN_PORT))
	retData = aisock.recv(65536)

	if retData == "FRUIT":
		print("PASS: Got FRUIT on AI input")
	else:
		print("FAILED!")
		NUMFAILED += 1
		
	retData = guisock.recv(65536)

	if retData == "FRUIT":
		print("PASS: Got FRUIT on GUI input")
	else:
		print("FAILED!")
		NUMFAILED += 1
		
	retData = statssock.recv(65536)

	if retData == "FRUIT":
		print("PASS: Got FRUIT on STATS input")
	else:
		print("FAILED!")
		NUMFAILED += 1


	print ("SEND: sending DEBUG from PACMAN")
	rand = random.randint(0,128)
	outsock.sendto("\xFE\x25" + "D" + chr(rand) + "somedebuginfo\xFF", (UDP_IP, PACMAN_PORT))
	retData = statssock.recv(65536)

	if retData == "&P:D" + chr(rand) + "somedebuginfo":
		print("PASS: Got DEBUG on STATS input")
	else:
		print("FAILED!")
		NUMFAILED += 1
		
		
		
	# send messages from GHOST
	# fruit
	rand = random.randint(0,128)
	print ("\n## GHOST I/O ##")
	print ("SEND: sending DEBUG from GHOST")
	outsock.sendto("\xFE\x25" + "D" + chr(rand) + "somedebuginfo\xFF", (UDP_IP, GHOST_PORT))
	retData = statssock.recv(65536)

	if retData == "&G:D" + chr(rand) +"somedebuginfo":
		print("PASS: Got DEBUG on STATS input")
	else:
		print("FAILED!")
		NUMFAILED += 1
	
RUN_IO_TESTS()
	
# ask user for repeat test looped

print("\nRun I/O tests continuous (100 iterations)? (y/N) ")
resp = raw_input().lower()

if resp == 'y' or resp == "yes":
	
	i = 0
	while i < 100:
		
		os.system('cls' if os.name == 'nt' else 'clear')
		
		print( "ITERATION - " + str(i))
				
		RUN_IO_TESTS()
		
		time.sleep(0.05)
		
		i += 1
		
else:
	pass
		
	
####################
#       END        #
#################### 

print("\n ########## TEST COMPLETE, NUMFAILED = %i ###########\n\n" % NUMFAILED)
