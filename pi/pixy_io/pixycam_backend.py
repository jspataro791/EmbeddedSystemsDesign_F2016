#!/usr/bin/env python3

###########################################################
#ECE 4525 - Group 18
#Author: Andrew Bryant
#
#This module is the framework for the Pixy Cam.
#It takes the data from the Pixy Cam module, interprets
#the instruction, and updates all relevant objects. 
#This includes identifying the playing board, where the 
#rovers are on the board, and assigning the rovers a node. 
############################################################

import sys
import time

BOARD_WIDTH = 24 #Actual Playing Board Width in Inches
BOARD_HEIGHT = 24 #Actual Playing Board Height in Inches
UPDATE = False# Flag to signal update
DIST_MARKER_FROM_BOARD = 2 #Inches the corner markers are from the board
NUM_ROW = 5 #Number of rows of nodes (5 gives one every 6")
NUM_COL = 5 #Number of columns of nodes (5 gives one every 6")
DEBUG = True #Flag for debugging purposes

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
	
inputFile = open("data1.txt") #Fake data from Pixy Cam
global expectedFile #Expected File
if(UPDATE):
	expectedFile = open("expected_data1.txt", 'w') 
else:
	expectedFile = open("expected_data1.txt")
	
#Convert one line of raw data to a location
def convertRawData():
	line = inputFile.readline()
	if(line == ''):
		sys.exit()
	line = line.split()

	if(line[0] == "0"):
		corner1.X = int(line[1])
		corner1.Y = int(line[2])
		print"Updated Corner 1 Data X: %i, Y: %i" %(corner1.X, corner1.Y)
		calc_board()
		print"Updated Board Center: (%i, %i)\n" %(board.center_X, board.center_Y)
		
		
	elif(line[0] == "1"):
		corner2.X = int(line[1])
		corner2.Y = int(line[2])
		print"Updated Corner 2 Data X: %i, Y: %i" %(corner2.X, corner2.Y)
		calc_board()
		print"Updated Board Center: (%i, %i)\n" %(board.center_X, board.center_Y)
		
	elif(line[0] == "2"):
		ghost.X = int(line[1])
		ghost.Y = int(line[2])
		node1 = calc_node(ghost.X, ghost.Y)
		ghost.nX = node1[0]
		ghost.nY = node1[1]
		print"Updated Ghost Rover Data X: %i, Y: %i" %(ghost.X, ghost.Y)
		print"Ghost Rover Node Is: (%i, %i)\n" %(ghost.nX, ghost.nY)

	elif(line[0] == "3"):
		user.X = int(line[1])
		user.Y = int(line[2])
		node2 = calc_node(user.X, user.Y)
		user.nX = node2[0]
		user.nY = node2[1]		
		print"Updated User Rover Data X: %i, Y: %i" %(user.X, user.Y)
		print"User Rover Node Is: (%i, %i)\n" %(user.nX, user.nY)
	#For updating file if global is flagged True
	if(UPDATE):
		if(line[0] == "0"):
			expectedFile.write('0: ' + str(corner1.X) + ' ' + str(corner1.Y) + ' ' + str(board.center_X) + ' ' + str(board.center_Y) + ' ' + str(board.width) + ' ' + str(board.height)+ ' ' + str(board.col_dist) + ' ' + str(board.row_dist) + '\n')
		elif(line[0] == "1"):
			expectedFile.write('1: ' + str(corner2.X) + ' ' + str(corner2.Y) + ' ' + str(board.center_X) + ' ' + str(board.center_Y) + ' ' + str(board.width) + ' ' + str(board.height) + ' ' + str(board.col_dist) + ' ' + str(board.row_dist) + '\n')
		elif(line[0] == "2"):
			expectedFile.write('2: ' + str(ghost.X) + ' ' + str(ghost.Y) + ' ' + str(ghost.nX) + ' ' + str(ghost.nY) + '\n')
		elif(line[0] == "3"):
			expectedFile.write('3: ' + str(user.X) + ' ' + str(user.Y) + ' ' + str(user.nX) + ' ' + str(user.nY) + '\n')		
	

def checkForCapture():
		if(abs(ghost.X - user.X) < 20 and abs(ghost.Y - user.Y) <20):
			user.C = True

		else:
			user.C = False
			
		if(UPDATE):
			expectedFile.write(str(user.C) + '\n')

#  name: test
#  @param NONE
#  @return NONE
#  description: Runs a test on previous update by comparing to the expected results 
def test():
	expected = expectedFile.readline()
	
	if(expected == 'True\n'):
		print "ERROR: PREVIOUS UPDATE SHOULD HAVE SIGNALED PACMAN CAPTURED BUT DID NOT"
	
	expected = expected.split()

	#Corner 1 Update
	if(expected[0] == '0:'):
		#Check if Corner 1 is updated correctly
		print "TEST: Expect: Corner 1 (X, Y) value: (%s, %s)" %(expected[1], expected[2])
		if(str(corner1.X) == expected[1] and str(corner1.Y) == expected[2]):
			print"    PASSED: Corner 1 (X, Y) value is at (%s, %s) \n" %(str(corner1.X), str(corner1.Y))
		else:
			print"    FAILED: Corner 1 (X, Y) value is at (%s, %s) \n" %(str(corner1.X), str(corner1.Y)) 
			
		#Check if Center of playing field is updated correctly
		print "TEST: Expect: Center of Playing Field: (%s, %s) " %(expected[3], expected[4])
		if(str(board.center_X) == expected[3] and str(board.center_Y) == expected[4]):
			print"    PASSED: Center of Playing Field is at (%s, %s) \n" %(str(board.center_X), str(board.center_Y))
		else:
			print"    FAILED: Center of Playing Field is at (%s, %s) \n" %(str(board.center_X), str(board.center_Y))
			
			
		#Check if Width and Height of playing field is updated correctly
		print "TEST: Expect: Width of Playing Field is %s, and Height is %s " %(expected[5], expected[6])
		if(str(board.width) == expected[5] and str(board.height) == expected[6]):
			print"    PASSED: Width of Playing Field is %s, and Height is %s \n" %(str(board.width), str(board.height))
		else:
			print"    FAILED: Width of Playing Field is %s, and Height is %s \n" %(str(board.width), str(board.height))
			
		#Check if width between columns and rows are correct
		print "TEST: Expect: Distance between columns: %s, and distance between rows: %s " %(expected[7], expected[8])
		if(str(board.col_dist) == expected[7] and str(board.row_dist) == expected[8]):
			print"    PASSED: Distance between columns is %s, and distance between rows is %s \n" %(str(board.col_dist), str(board.row_dist))
		else:
			print"    FAILED: Distance between columns: %s, and distance between rows: %s \n" %(str(board.col_dist), str(board.row_dist))

	#Corner 2 Update
	elif(expected[0] == '1:'):
		#Check if Corner 2 is updated correctly
		print "TEST: Expect: Corner 2 (X, Y) value: (%s, %s)" %(expected[1], expected[2])
		if(str(corner2.X) == expected[1] and str(corner2.Y) == expected[2]):
			print"    PASSED: Corner 2 (X, Y) value is at (%s, %s) \n" %(str(corner2.X), str(corner2.Y))
		else:
			print"    FAILED: Corner 2 (X, Y) value is at (%s, %s) \n" %(str(corner2.X), str(corner2.Y)) 

		#Check if Center of playing field is updated correctly
		print "TEST: Expect: Center of Playing Field: (%s, %s) " %(expected[3], expected[4])
		if(str(board.center_X) == expected[3] and str(board.center_Y) == expected[4]):
			print"    PASSED: Center of Playing Field is at (%s, %s) \n" %(str(board.center_X), str(board.center_Y))
		else:
			print"    FAILED: Center of Playing Field is at (%s, %s) \n" %(str(board.center_X), str(board.center_Y))
			
			
		#Check if Width and Height of playing field is updated correctly
		print "TEST: Expect: Width of Playing Field is %s, and Height is %s " %(expected[5], expected[6])
		if(str(board.width) == expected[5] and str(board.height) == expected[6]):
			print"    PASSED: Width of Playing Field is %s, and Height is %s \n" %(str(board.width), str(board.height))
		else:
			print"    FAILED: Width of Playing Field is %s, and Height is %s \n" %(str(board.width), str(board.height))
			
		#Check if width between columns and rows are correct
		print "TEST: Expect: Distance between columns: %s, and distance between rows: %s " %(expected[7], expected[8])
		if(str(board.col_dist) == expected[7] and str(board.row_dist) == expected[8]):
			print"    PASSED: Distance between columns is %s, and distance between rows is %s \n" %(str(board.col_dist), str(board.row_dist))
		else:
			print"    FAILED: Distance between columns: %s, and distance between rows: %s \n" %(str(board.col_dist), str(board.row_dist))

					
	#Ghost Rover Update
	elif(expected[0] == '2:'):
		#Check that rover location was properly updated
		print "TEST: Expect: Ghost Rover (X, Y) value: (%s, %s)" %(expected[1], expected[2])
		if(str(ghost.X) == expected[1] and str(ghost.Y) == expected[2]):
			print"    PASSED: Ghost Rover (X, Y) value is at (%s, %s) \n" %(str(ghost.X), str(ghost.Y))
		else:
			print"    FAILED: Ghost Rover (X, Y) value is at (%s, %s) \n" %(str(ghost.X), str(ghost.Y)) 

		#Check that rover nodal assignment worked properly
		print "TEST: Expect: Ghost Rover Nodal Assignment to be (%s, %s)" %(expected[3], expected[4])
		if(str(ghost.nX) == expected[3] and str(ghost.nY) == expected[4]):
			print"    PASSED: Ghost Rover Nodal Assignment is (%s, %s)\n" %(str(ghost.nX), str(ghost.nY))
		else:
			print"    FAILED: Ghost Rover Nodal Assignment is (%s, %s)\n" %(str(ghost.nX), str(ghost.nY))

			
	
	#User Rover Update
	elif(expected[0] == '3:'):
		#Check that rover location was properly updated
		print "TEST: Expect: Pacman Rover (X, Y) value: (%s, %s)" %(expected[1], expected[2])
		if(str(user.X) == expected[1] and str(user.Y) == expected[2]):
			print"    PASSED: Pacman Rover (X, Y) value is at (%s, %s) \n" %(str(user.X), str(user.Y))
		else:
			print"    FAILED: Pacman Rover (X, Y) value is at (%s, %s) \n" %(str(user.X), str(user.Y)) 
						
		#Check that rover nodal assignment worked properly
		print "TEST: Expect: Pacman Rover Nodal Assignment to be (%s, %s)" %(expected[3], expected[4])
		if(str(user.nX) == expected[3] and str(user.nY) == expected[4]):
			print"    PASSED: Pacman Rover Nodal Assignment is (%s, %s)\n" %(str(user.nX), str(user.nY))
		else:
			print"    FAILED: Pacman Rover Nodal Assignment is (%s, %s)\n" %(str(user.nX), str(user.nY))
		
	#Check that rover caught assignment worked properly
	caught = expectedFile.readline()
	print "TEST: Expect: Rover Caught Assignment: %s" % caught.strip()
	if((str(user.C)+'\n') == caught):
		print"    PASSED: Rover Caught Assignment is %s \n" %str(user.C)
	else:
		print"    FAILED: Rover Caught Assignment is %s \n" %str(user.C)

	#Momentarily pause after testing instruction finished 
	time.sleep(1)

		
		
def main():
	#Convert one instruction at a time and evaluate 
	while(True):
		
		#Convert Raw Data
		convertRawData()
		
		#Check if Rover is Captured
		checkForCapture()
		
		#Test Against Expected Data
		if(DEBUG):
			test()
		
		
main()
