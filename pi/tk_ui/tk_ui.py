from tkinter import *
import time
import sys
import socket

# Server stuff

host = ''
router_ip = 'localhost'
port = 50000
router_port = 10000
router = (router_ip,router_port)
size = 1024
s = None

try:
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.bind((host,port))
	s.setblocking(0)
except socket.error as message:
	if s:
		s.close()
	print ("Could not open socket: " + str(message))
	sys.exit(1)

def cb(textbox, text):
	textbox.insert(END, text)
	textbox.see(END)
	s.sendto(text.encode(), router)
	print(text)

def callback(button, text):
	if button == "left":
		return lambda : cb(text, "SEND to PACMAN: TURN LEFT\n")
	elif button == "right":
		return lambda : cb(text, "SEND to PACMAN: TURN RIGHT\n")
	elif button == "180":
		return lambda : cb(text, "SEND to PACMAN: TURN 180\n")
	else:
		return lambda : cb(text, "SEND to PACMAN: ?\n")

# GUI stuff
   
root = Tk()
root.title("Pacman Control")

#mainframe = Frame(root, padding="20 20 20 20")
mainframe = Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

text = Text(mainframe, width=60, height=8)
text.grid(column=1, row=3, columnspan=3, sticky=S)

label_str = StringVar()
label = Label(mainframe, textvariable=label_str, relief=RAISED)
label.grid(column=2, row=2, sticky=S)

Button(mainframe, text="Left", command=callback("left", text)).grid(column=1, row=1, sticky=E)
Button(mainframe, text="180°", command=callback("180", text)).grid(column=2, row=1)
Button(mainframe, text="Right", command=callback("right", text)).grid(column=3, row=1, sticky=W)


for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

fruit = False
label_str.set("              ")
start = 0

while True:
	if fruit and (time.time() - start >= 30):
		fruit = False
		label_str.set("              ")

	try:
		root.update_idletasks()
		root.update()
	except Exception as e:
		print("Error: GUI Crashed (or closed): ", str(e))
		sys.exit(1)

	try:
		data, address = s.recvfrom(size)
		if data:
			#client.send(data)
			text.insert(END, data.decode("utf-8")+'\n')
			text.see(END)
			if data == b'FRUIT!':
				print("FRUIT!\n")
				fruit = True
				start = time.time()
				label_str.set("FRUIT OBTAINED")
	except socket.error:
		pass