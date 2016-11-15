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
UPDATE = False
#Inches the corner markers are from the board
DIST_MARKER_FROM_BOARD = 2 
#Number of rows of nodes (5 gives one every 6")
NUM_ROW = 5
#Number of columns of nodes (5 gives one every 6") 
NUM_COL = 5
#Distance required for ghost to capture user
CAUGHT_DIST = 30

#Corner Class
#
#Keep track of the location of the corner tags
class Corner:
	X = 0
	Y = 0

corner1 = Corner() # Corner 1 Object for top left, ID 0 in data
corner2 = Corner() # Corner 2 Object for bottom right, ID 1 in data

#Rover Class
#
#Keep track of ghost and user rover's location, node, and caught status
class Rover:
	X = 0
	Y = 0
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
		corner1.X = blocks[index].x;
		corner1.Y = blocks[index].y;
		print"Updated Corner 1 Data X: %i, Y: %i" %(corner1.X, corner1.Y)
		calc_board()
		print"Updated Board Center: (%i, %i)\n" %(board.center_X, board.center_Y)
		
	#Update Corner 2
	elif(blocks[index].signature == 2):
		corner2.X = blocks[index].x;
		corner2.Y = blocks[index].y;
		print"Updated Corner 2 Data X: %i, Y: %i" %(corner2.X, corner2.Y)
		calc_board()
		print"Updated Board Center: (%i, %i)\n" %(board.center_X, board.center_Y)
		
	#Update Ghost Rover
	elif(blocks[index].signature == 3):
		ghost.X = blocks[index].x
		ghost.Y = blocks[index].y
		node1 = calc_node(ghost.X, ghost.Y)
		ghost.nX = node1[0]
		ghost.nY = node1[1]
		print"Updated Ghost Rover Data X: %i, Y: %i" %(ghost.X, ghost.Y)
		print"Ghost Rover Node Is: (%i, %i)\n" %(ghost.nX, ghost.nY)
		
		
	#Update User Rover
	elif(blocks[index].signature == 4):
		user.X = blocks[index].x
		user.Y = blocks[index].y
		node2 = calc_node(user.X, user.Y)
		user.nX = node2[0]
		user.nY = node2[1]
		print"Updated User Rover Data X: %i, Y: %i" %(user.X, user.Y)
		print"User Rover Node Is: (%i, %i)\n" %(user.nX, user.nY)
		
#	name: checkForCapture
#	@param NONE
#	@return NONE
#	description: Check if the Ghost Rover and User Rover are close enough to warrant capture
def checkForCapture():
		if(abs(ghost.X - user.X) < CAUGHT_DIST and abs(ghost.Y - user.Y) < CAUGHT_DIST):
			user.C = True
			print "Captured"

		else:
			user.C = False
			print "Not Captured"
		
# Wait for blocks #
while 1:

  count = pixy_get_blocks(100, blocks)

  if count > 0:
    # Blocks found #
    for index in range (0, count):
		print "Raw Data:"
		print '[BLOCK_TYPE=%d SIG=%d X=%3d Y=%3d WIDTH=%3d HEIGHT=%3d]' % (blocks[index].type, blocks[index].signature, blocks[index].x, blocks[index].y, blocks[index].width, blocks[index].height)
		convertRawData(index);
		checkForCapture()

