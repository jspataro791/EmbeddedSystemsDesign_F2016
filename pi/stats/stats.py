#!/usr/bin/python2.7

#############################################################
#                   ::STATS SOFTWARE::                      #
#                                                           #
#    Desc: Displays statistics info about rover system      #
#           and other functions/processes                   #
#    Author: John Spataro                                   #
#    Date: 10/12/2016                                       #
#                                                           #
#############################################################

GLOBAL_DEBUG = True

####################
#      IMPORTS     #
####################

import os
import time
import socket
import ConfigParser

cparse = ConfigParser.ConfigParser()
cparse.read("../common/conf/ports.conf")

logfile = open("../log/stats.log","w")

startTime = time.time()

printList = []

####################
#    CONSTANTS     #
####################

UDP_IP = cparse.get("IOPORTS","UDP_IP")
ROUTER_INPUT_PORT = cparse.getint("STATSPORTS","ROUTING_INPUT_PORT")
AI_INPUT_PORT = cparse.getint("STATSPORTS", "AI_INPUT_PORT")
PIXYCAM_IO_INPUT_PORT = cparse.getint("STATSPORTS", "PIXYCAM_IO_INPUT_PORT")

DBG_MSG_ROLLOVER = 127


####################
#    FUNCTIONS     #
####################

def dbgPrint(dtype, msg):
        if GLOBAL_DEBUG is True:
                print("- " + dtype + ": " + msg)

def clearScreen():
        os.system('cls' if os.name == 'nt' else 'clear')

def debugDataPrinter(dbgData):
        if len(printList) > 8:
                printList = []
        print(dbgData)
        global printList
        printList.append(dbgData)              
        global logfile
        global startTime
        curTime = format(time.time() - startTime, ".2f")
        logfile.write(str(curTime) + ", " + dbgData + "\n")

def openUDPSocket(IP, PORT, IO_INTENT):

        retry = 1

        while(1):
                try:
                        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                        sock.setblocking(0)

                        if IO_INTENT is "READ":
                                sock.bind((IP, PORT))
                        elif IO_INTENT is "WRITE":
                                sock.connect((IP, PORT))
                        else:
                                raise IOError("Invalid IO intent for %s:%i" % (IP,PORT))
                
                        debugDataPrinter("SOCK: Opened socket %s:%i in mode %s" % (IP, PORT, IO_INTENT))
                        
                        return sock
                except IOError as e:
                        if retry is 5:
                                print(e)
                                exit(0)
                        else:
                                retry += 1
                                

                  

                
####################
#     GLOBALS      # 
####################

PAC_CUR_DIR = "LEFT"
GHOST_CUR_DIR = "LEFT"
GHOST_CUR_SPEED = 0
NUM_FRUITS = 0
FRUIT_STAT = False
PAC_MISSED_MSG = 0
GHOST_MISSED_MSG = 0

pacDbgLast = 0
pacDbgMissing = 0
pacDbgFirst = True
ghostDbgLast = 0
ghostDbgMissing = 0
ghostDbgFirst = True


#######################################
#                MAIN                 #
#######################################

if __name__ == "__main__":
        
        # clearscreen
        clearScreen()
        
        # welcome
        print("[ STARTING STATS VIEW ]\n")

        # open input sockets
        ROUTER_LISTEN = openUDPSocket(UDP_IP, ROUTER_INPUT_PORT, "READ")
        AI_LISTEN = openUDPSocket(UDP_IP, AI_INPUT_PORT, "READ")
        PIXYCAM_IO_LISTEN = openUDPSocket(UDP_IP, PIXYCAM_IO_INPUT_PORT, "READ")
        
        # main loop
        
        while True:
              
                time.sleep(0.1)
              
                clearScreen()
                
                
                                
                print("PAC DIR: %s, GHOST DIR: %s, GHOST SPD: %i" % (PAC_CUR_DIR, GHOST_CUR_DIR, GHOST_CUR_SPEED))
                print("PAC MSG MISSING: %i, GHOST MSG MISSING %i" % (pacDbgMissing, ghostDbgMissing))
                print("NUM FRUITS: %i" % NUM_FRUITS)
                print("----------------------------------------------------------------------")
                
                for x in range(len(printList)):
                        print(printList[x])
                           
                # get stuff from ports
              
                try:
                        routData = ROUTER_LISTEN.recv(65536)
                except socket.error:
                        routData = ""
                        pass
                        
                try:
                        aiData = AI_LISTEN.recv(65536)
                except socket.error:
                        aiData = ""
                        pass
                        
                try:
                        pixyioData = PIXYCAM_IO_LISTEN.recv(65536)
                except socket.error:
                        pixyioData = ""
                        pass
                        
                # parse router data
                
                if routData[0:3] == "&P:":
                        if routData[3] == "D":
                                # check on message number
                                pacDbgNew = ord(routData[4])
                            
                           
                                if pacDbgFirst == False:

                                        if pacDbgNew > pacDbgLast:

                                                diff = pacDbgNew - pacDbgLast

                                                if diff < 0:
                                                        pacDbgMissing += diff + DBG_MSG_ROLLOVER
                                                else:
                                                        pacDbgMissing += diff - 1
                                
                                                                
                                else:
                                        pacDbgMissing = 0
                                        
                                pacDbgFirst = False
                                pacDbgLast = pacDbgNew
                                
                                # print the debug information
                                
                                debugDataPrinter("PACMAN: " + routData[5:])
                        elif routData[3:] == "LEFT":
                                debugDataPrinter("PACMAN: Instructed to turn LEFT")
                                PAC_CUR_DIR = "LEFT"
                                
                        elif routData[3:] == "RIGHT":
                                debugDataPrinter("PACMAN: Instructed to turn RIGHT")
                                PAC_CUR_DIR = "RIGHT"

                if routData[0:3] == "&G:":
                        if routData[3] == "D":
                                # check on message number
                                ghostDbgNew = ord(routData[4])
                            
                           
                                if ghostDbgFirst == False:

                                        if ghostDbgNew > ghostDbgLast:

                                                diff = ghostDbgNew - ghostDbgLast

                                                if diff < 0:
                                                        ghostDbgMissing += diff + DBG_MSG_ROLLOVER
                                                else:
                                                        ghostDbgMissing += diff - 1
                                
                                                                
                                else:
                                        ghostDbgMissing = 0
                                        
                                ghostDbgFirst = False
                                ghostDbgLast = ghostDbgNew
                                
                                # print the debug information
                                
                                debugDataPrinter("GHOST: " + routData[5:])
                        elif routData[3:] == "LEFT":
                                debugDataPrinter("GHOST: Instructed to turn LEFT")
                                PAC_CUR_DIR = "LEFT"
                                
                        elif routData[3:] == "RIGHT":
                                debugDataPrinter("GHOST: Instructed to turn RIGHT")
                                PAC_CUR_DIR = "RIGHT"

                if routData == "FRUIT":
                        debugDataPrinter("PACMAN: Found a fruit!")
                        NUM_FRUITS += 1
        
        
                if routData == "EXIT":
                        debugDataPrinter("EXITING")
                        exit()
        
                # parse AI data
                if aiData != "":
                        debugDataPrinter("GUI: " + aiData)
                
                # parse PIXIO data
                if pixyioData != "":
                        debugDataPrinter("PIXY_IO: " + pixyioData) 
                        
