#!/usr/bin/env python2

###########################################################
#ECE 4525 - Group 18
#Author: Andrew Bryant
#
#This module is the framework for the Pixy Cam.
#It takes the data from the Pixy Cam module, interprets
#the instruction, and updates all relevant objects. 
#This includes identifying the playing board, where the 
#rovers are on the board, if the user rover is caught,
#and assigning the rovers a node. 
############################################################

import sys
import time

from pixy import *
from ctypes import *

from Pathfinder import *

logFile = open("pixy_log_file.txt", 'w') 

# Initialize Pixy Interpreter thread #
pixy_init()



######################################
#Flag for debugging purposes
DEBUG = True 
######################################

#Actual Playing Board Width in Inches
BOARD_WIDTH = 24 
#Actual Playing Board Height in Inches
BOARD_HEIGHT = 24 
#Flag to signal update
UPDATE = 0
#Inches the corner markers are from the board
DIST_MARKER_FROM_BOARD = 0
#Number of rows of nodes (5 gives one every 6")
NUM_ROW = 6
#Number of columns of nodes (5 gives one every 6") 
NUM_COL = 6
#Distance required for ghost to capture user
CAUGHT_DIST = 30
#Maximum distance allowed for a code to jump to be counted(X or Y direction)
MAX_JUMP = 20


#Corner Class
#
#Keep track of the location of the corner tags
class Corner:
	X = -1
	Y = -1
	pX = []
	pY = []
	count = 0

corner1 = Corner() # Corner 1 Object for top left, ID 0 in data
corner2 = Corner() # Corner 2 Object for bottom right, ID 1 in data

#Rover Class
#
#Keep track of ghost and user rover's location, node, and caught status
class Rover:
	X = -1
	Y = -1
	nX = -1
	nY = -1
	pX = []
	pY = []
	C = False
	count = 0
	
ghost = Rover() #Ghost Rover Object, ID 2 in data
user = Rover() #User Rover Object, ID 3 in data

#Board Class
#
#Keep track of the properties and location of the playing field
class Board:
	center_X = 0 #X value for the center of the playing field
	center_Y = 0 #Y value for the center of the playing field
	width = 0 #Width of playing field in image
	height = 0 #Height of playing field in image
	col_dist = 0 #distance between columns in image
	row_dist = 0 #distance between rows in image
	#Distance required for ghost to capture user
	CAUGHT_DIST = (col_dist + row_dist)/4
	
board = Board() #Playing Board Object

def average(l):
	if(len(l) > 0):
		avg = sum(l)/len(l)
		return avg

#Calculate the various values for the playing field
def calc_board():
	board.center_X = corner1.X + ((corner2.X - corner1.X)/2)
	board.center_Y = corner1.Y + ((corner2.Y - corner1.Y)/2)
	board.width = abs(corner1.X - corner2.X)
	board.height = abs(corner1.Y - corner2.Y)
	board.col_dist = board.width / (NUM_COL-1)
	board.row_dist = board.height / (NUM_ROW-1)
	
#Determine which node the x, y coordinate is closest too. 
def calc_node(x, y):
	nodeX = -1
	nodeY = -1
	for i in range(0, NUM_COL):
		if(abs(board.center_X - (board.width/2) + (i*board.col_dist) - x) < (board.col_dist*2/5)):
			nodeX = i

	for j in range(0, NUM_ROW):
		if(abs(board.center_Y - (board.height/2) + (j*board.row_dist) - y) < (board.row_dist*2/5)):
			nodeY = j
        return [nodeX, nodeY]




#Blocks Class
class Blocks (Structure):
	_fields_ = [ ("type", c_uint),
               ("signature", c_uint),
               ("x", c_uint),
               ("y", c_uint),
               ("width", c_uint),
               ("height", c_uint),
               ("angle", c_uint) ]

blocks = BlockArray(100)

#Convert raw data and assign values to rover / corner object
def convertRawData(index):
	#Update Corner 1
	if(blocks[index].signature == 1):
		if((abs(corner1.X - blocks[index].x) < MAX_JUMP and abs(corner1.Y - blocks[index].y) < MAX_JUMP) or corner1.X < 0) :
			
			corner1.pX.append(blocks[index].x)
			corner1.pY.append(blocks[index].y)
			if(len(corner1.pX) > 10):
				corner1.pX.pop(0)
			if(len(corner1.pY) > 10):
				corner1.pY.pop(0)
			corner1.X = average(corner1.pX)
			corner1.Y = average(corner1.pY)
						
			#print"Updated Corner 1 Data X: %i, Y: %i" %(corner1.X, corner1.Y)
			calc_board()
			#print"Updated Board Center: (%i, %i)\n" %(board.center_X, board.center_Y)
			#logFile.write("Updated Corner 1 Data X: %i, Y: %i\n" %(corner1.X, corner1.Y))
			#logFile.write("Updated Board Center: (%i, %i)\n" %(board.center_X, board.center_Y))		
		
					
					
	#Update Corner 2
	elif(blocks[index].signature == 2):
		if((abs(corner2.X - blocks[index].x) < MAX_JUMP and abs(corner2.Y - blocks[index].y) < MAX_JUMP) or corner2.X < 0) :

			corner2.pX.append(blocks[index].x)
			corner2.pY.append(blocks[index].y)
			if(len(corner2.pX) > 10):
				corner2.pX.pop(0)
			if(len(corner2.pY) > 10):
				corner2.pY.pop(0)
			corner2.X = average(corner2.pX)
			corner2.Y = average(corner2.pY)
			
			#print"Updated Corner 2 Data X: %i, Y: %i" %(corner2.X, corner2.Y)
			calc_board()
			#print"Updated Board Center: (%i, %i)\n" %(board.center_X, board.center_Y)
			#logFile.write("Updated Corner 2 Data X: %i, Y: %i\n" %(corner2.X, corner2.Y))
			#logFile.write("Updated Board Center: (%i, %i)\n" %(board.center_X, board.center_Y))		
		
	#Update Ghost Rover
	elif(blocks[index].signature == 3):
		if((abs(ghost.X - blocks[index].x) < MAX_JUMP and abs(ghost.Y - blocks[index].y) < MAX_JUMP) or ghost.X < 0) :
			"""
			ghost.pX.append(blocks[index].x)
			ghost.pY.append(blocks[index].y)
			if(len(ghost.pX) > 10):
				ghost.pX.pop(0)
			if(len(ghost.pY) > 10):
				ghost.pY.pop(0)
			ghost.X = average(ghost.pX)
			ghost.Y = average(ghost.pY)
			"""
			ghost.X = blocks[index].x
			ghost.Y = blocks[index].y
			
			
		else: 
			#print("Ghost Rover update ignored because of large jump")
			return False
		

		node1 = calc_node(ghost.X, ghost.Y)
					
		if ((node1[0] != ghost.nX or node1[1] != ghost.nY) and (node1[0] > -1 and node1[1] > -1)):
			UPDATE = 1
			ghost.nX = node1[0]
			ghost.nY = node1[1]
			print"Updated Ghost Rover Data X: %i, Y: %i" %(ghost.X, ghost.Y)
			print"Ghost Rover Node Is: (%i, %i)\n" %(ghost.nX, ghost.nY)
			logFile.write("Updated Ghost Rover Data X: %i, Y: %i \n" %(ghost.X, ghost.Y))
			logFile.write("Ghost Rover Node Is: (%i, %i)\n" %(ghost.nX, ghost.nY))
			return True
		else:
			return False

		
	#Update User Rover
	elif(blocks[index].signature == 4):
		user.count += 1
		if((abs(user.X - blocks[index].x) < MAX_JUMP and abs(user.Y - blocks[index].y) < MAX_JUMP) or user.X < 0) :
			"""
			user.pX.append(blocks[index].x)
			user.pY.append(blocks[index].y)
			if(len(user.pX) > 10):
				user.pX.pop(0)
			if(len(user.pY) > 10):
				user.pY.pop(0)
			user.X = average(user.pX)
			user.Y = average(user.pY)
			"""
			user.X = blocks[index].x
			user.Y = blocks[index].y
			
		else:
			#print("User Rover update ignored because of large jump")
			return False
		
		
		node2 = calc_node(user.X, user.Y)
		
		
		if ((node2[0] != user.nX or node2[1] != user.nY) and (node2[0] > -1 and node2[1] > -1)):
			UPDATE = 1
			user.nX = node2[0]
			user.nY = node2[1]
			print"Updated User Rover Data X: %i, Y: %i" %(user.X, user.Y)
			print"User Rover Node Is: (%i, %i)\n" %(user.nX, user.nY)
			logFile.write("Updated User Rover Data X: %i, Y: %i \n" %(user.X, user.Y))
			logFile.write("User Rover Node Is: (%i, %i)\n" %(user.nX, user.nY))
			return True
			
		else:
			return False
				
#	name: checkForCapture
#	@param NONE
#	@return NONE
#	description: Check if the Ghost Rover and User Rover are close enough to warrant capture
def checkForCapture():
		if(abs(ghost.X - user.X) < CAUGHT_DIST and abs(ghost.Y - user.Y) < CAUGHT_DIST):
			user.C = True
			print "Captured"
			pathfinder.captured()

		else:
			user.C = False
			#print "Not Captured"
			
pathfinder = Pathfinder()
# Wait for blocks #
while 1:

  count = pixy_get_blocks(100, blocks)

  if count > 0:
    # Blocks found #
    for index in range (0, count):
		#print"Message Queue Size %d" % count
		#print "Raw Data:"
		#print '[BLOCK_TYPE=%d SIG=%d X=%3d Y=%3d WIDTH=%3d HEIGHT=%3d]' % (blocks[index].type, blocks[index].signature, blocks[index].x, blocks[index].y, blocks[index].width, blocks[index].height)
		if (convertRawData(index)):
			UPDATE = 1
			print(UPDATE)
		if((user.nX >= 0) and (ghost.nX >= 0) and (corner1.X >= 0) and (corner2.Y >= 0)):
			checkForCapture()
			d = [ghost.nX, ghost.nY, user.nX, user.nY]
			if UPDATE == 1:
				print("update happened")
				print ("C1: %d,%d C2: %d,%d G: %d,%d U: %d,%d" % (corner1.X, corner1.Y, corner2.X, corner2.Y, ghost.X, ghost.Y, user.X, user.Y) )
				pathfinder.update_locations(d)
				UPDATE = 0
