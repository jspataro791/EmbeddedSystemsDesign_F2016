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
BOARD_WIDTH = 30
#Actual Playing Board Height in Inches
BOARD_HEIGHT = 22.5 
#Flag to signal update
UPDATE = False
#Inches the corner markers are from the board
DIST_MARKER_FROM_BOARD = 3
#Number of rows of nodes (5 gives one every 6")
NUM_ROW = 4
#Number of columns of nodes (5 gives one every 6") 
NUM_COL = 5
#Distance required for ghost to capture user
CAUGHT_DIST = 40
#Maximum distance allowed for a code to jump to be counted(X or Y direction)
MAX_JUMP = 20


#Corner Class
#
#Keep track of the location of the corner tags
class Corner:
	X = -1
	Y = -1

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
	C = False
	
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
	nodeX = 0
	nodeY = 0
	for i in range(0, NUM_COL):
		if(abs(board.center_X - (board.width/2) + (i*board.col_dist) - x) < (board.col_dist/2)):
			nodeX = i
	
	for j in range(0, NUM_ROW):
		if(abs(board.center_Y - (board.height/2) + (j*board.row_dist) - y) < (board.row_dist/2)):
			nodeY = j
			
	return (nodeX, nodeY)




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
                        corner1.X = blocks[index].x;
                        corner1.Y = blocks[index].y;
                else:
                        return False#		print"Updated Corner 1 Data X: %i, Y: %i" %(corner1.X, corner1.Y)
		calc_board()
#		print"Updated Board Center: (%i, %i)\n" %(board.center_X, board.center_Y)
#		logFile.write("Updated Corner 1 Data X: %i, Y: %i\n" %(corner1.X, corner1.Y))
#		logFile.write("Updated Board Center: (%i, %i)\n" %(board.center_X, board.center_Y))
		return False
                
	#Update Corner 2
	elif(blocks[index].signature == 2):
                if((abs(corner2.X - blocks[index].x) < MAX_JUMP and abs(corner2.Y - blocks[index].y) < MAX_JUMP) or corner2.X < 0) :
                        corner2.X = blocks[index].x;
                        corner2.Y = blocks[index].y;
                else:
                        return False
#		print"Updated Corner 2 Data X: %i, Y: %i" %(corner2.X, corner2.Y)
		calc_board()
#		print"Updated Board Center: (%i, %i)\n" %(board.center_X, board.center_Y)
#		logFile.write("Updated Corner 2 Data X: %i, Y: %i\n" %(corner2.X, corner2.Y))
#		logFile.write("Updated Board Center: (%i, %i)\n" %(board.center_X, board.center_Y))
                return False
		
	#Update Ghost Rover
	elif(blocks[index].signature == 3):
                if((abs(ghost.X - blocks[index].x) < MAX_JUMP and abs(ghost.Y - blocks[index].y) < MAX_JUMP) or ghost.X < 0) :
                        ghost.X = blocks[index].x
                        ghost.Y = blocks[index].y
                        checkForCapture()
		else:
                        return False
                node1 = calc_node(ghost.X, ghost.Y)
                if((ghost.nX != node1[0]) or (ghost.nY != node1[1])):
                        ghost.nX = node1[0]
                        ghost.nY = node1[1]
                        return True
                else:
                        return False
#		print"Updated Ghost Rover Data X: %i, Y: %i" %(ghost.X, ghost.Y)
#		print"Ghost Rover Node Is: (%i, %i)\n" %(ghost.nX, ghost.nY)
#		logFile.write("Updated Ghost Rover Data X: %i, Y: %i \n" %(ghost.X, ghost.Y))
#		logFile.write("Ghost Rover Node Is: (%i, %i)\n" %(ghost.nX, ghost.nY))
		
	#Update User Rover
	elif(blocks[index].signature == 4):
                if((abs(user.X - blocks[index].x) < MAX_JUMP and abs(user.Y - blocks[index].y) < MAX_JUMP) or user.X < 0) :
                        user.X = blocks[index].x
                        user.Y = blocks[index].y
                        checkForCapture()
                else:
                        return False
		node2 = calc_node(user.X, user.Y)
                if ((user.nX != node2[0]) or (user.nY != node2[1])):
                        user.nX = node2[0]
                        user.nY = node2[1]
                        return True
                else:
                        return False
#		print"Updated User Rover Data X: %i, Y: %i" %(user.X, user.Y)
#		print"User Rover Node Is: (%i, %i)\n" %(user.nX, user.nY)
#		logFile.write("Updated User Rover Data X: %i, Y: %i \n" %(user.X, user.Y))
#		logFile.write("User Rover Node Is: (%i, %i)\n" %(user.nX, user.nY))
				
#	name: checkForCapture
#	@param NONE
#	@return NONE
#	description: Check if the Ghost Rover and User Rover are close enough to warrant capture
def checkForCapture():
		if(abs(ghost.X - user.X) < CAUGHT_DIST and abs(ghost.Y - user.Y) < CAUGHT_DIST):
			user.C = True
			print "Captured"
			pathfinder.captured()
                        while(1): 
                                pass

		else:
			user.C = False

			
pathfinder = Pathfinder()
# Wait for blocks #
while 1:
  count = pixy_get_blocks(100, blocks)
  UPDATE = 0
  if count > 0:
    # Blocks found #
    for index in range (0, count):
        UPDATE = 0
        if(convertRawData(index)):
                UPDATE = 1
        if((user.X >= 0) and (ghost.X >= 0)):
                checkForCapture()
                if(UPDATE == 1):
                        d = [ghost.nX, ghost.nY, user.nX, user.nY]
                        pathfinder.update_locations(d)

