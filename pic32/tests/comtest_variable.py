import socket
import os
import sys
import time

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect(('10.0.0.191', 2000))


time.sleep(1)


    
s.send("\xFE\xFE\xFE\x07" + "D" + chr(0) + "S" + chr(16) + "G" + chr(1) + "E" + "\xFF\xFF")
