import pickle
import socketserver
import threading
import os
import sys
import socket
import random
import time

sock = 0
server = 0
HOST = "0.0.0.0"
PORT = 42069
#grid = [["*"]*7]*6
grid = [["*","*","*","*","*","*","*"],["*","*","*","*","*","*","*"],["*","*","*","*","*","*","*"],["*","*","*","*","*","*","*"],["*","*","*","*","*","*","*"],["*","*","*","*","*","*","*"]]
player = 0
opponent = 0
turncount = 1
turnTaken = 0

finished = "*"

def is_number(n):
    try:
        float(n)
        return True
    except ValueError:
        return False

def clear():
	os.system("cls")
	pass

def checkWon(g):
	global finished

	x = len(g[0])
	y = len(g)
	
	# HORIZONTAL
	# each col
	for i in range(0, x-3):
		# each row
		for j in range(0, y):
			if(g[j][i] != "*" and g[j][i] == g[j][i+1] and g[j][i+1] == g[j][i+2] and g[j][i+2] == g[j][i+3]):
				finished = g[j][i]
				return finished
	
	# VERTICAL
	# each col
	for i in range(0, x):
		# each row
		for j in range(0, y-3):
			if(g[j][i] != "*" and g[j][i] == g[j+1][i] and g[j+1][i] == g[j+2][i] and g[j+2][i] == g[j+3][i]):
				finished = g[j][i]
				return finished
	
	# DIAGONAL \
	# each col
	for i in range(0, x-3):
		# each row
		for j in range(0, y-3):
			if(g[j][i] != "*" and g[j][i] == g[j+1][i+1] and g[j+1][i+1] == g[j+2][i+2] and g[j+2][i+2] == g[j+3][i+3]):
				finished = g[j][i]
				return finished
	
	# DIAGONAL /
	# each col
	for i in range(0, x-3):
		# each row
		for j in range(0+3, y):
			if(g[j][i] != "*" and g[j][i] == g[j-1][i+1] and g[j-1][i+1] == g[j-2][i+2] and g[j-2][i+2] == g[j-3][i+3]):
				finished = g[j][i]
				return finished
	
	return finished

class MyTCPHandler(socketserver.BaseRequestHandler):
	
	def handle(self):
		global opponent
		global turncount
		global grid
		global player
		# self.request is the TCP socket connected to the client
		self.data = pickle.loads(self.request.recv(1024))
		#print("{} sent:".format(self.client_address[0]))
		#print(self.data)

		# initial connection
		if self.data[0] == 0:
			
			# randomly choose who goes first (1 goes first and is O; 0 goes second and is X)
			#turnOrder = random.randint(0,1)
			turnOrder = 1
			if(turnOrder == 1):
				player = "O"
				opponent = "X"
			else:
				player = "X"
				opponent = "O"
				
			self.request.sendall(pickle.dumps([opponent]))
		
		# client is taking their turn
		if self.data[0] == 1:
			# add new token to board
			invalid = True
			for i in range(5, -1, -1):
				#print(i,self.data[1]-1)
				if(grid[i][self.data[1]-1] == "*"):
					grid[i][self.data[1]-1] = opponent
					invalid = False
					turncount += 1
					break
				
			#print(invalid)
			self.request.sendall(pickle.dumps([invalid,grid,turncount]))
			
		# client is waiting for server to take their turn
		if self.data[0] == 2:
			self.request.sendall(pickle.dumps([turncount, grid, checkWon(grid)]))

def c4Server():
	HOST, PORT = "0.0.0.0", 42069

	# Create the server, binding to localhost on port 42069
	server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)

	with server:
		server_thread = threading.Thread(target=server.serve_forever)
		server_thread.daemon = True
		server_thread.start()
		#print("Server loop running in thread:", server_thread.name)

		# game goes here
		global player
		global grid
		global finished
		global turncount
		
		clear()
		print("WAITING FOR OTHER PLAYER...")
		
		# wait until other player joins
		while(player == 0):
			pass
		
			
		while(finished == "*"):		
			if(printGrid(grid)):
			# your turn
				invalid = True
				while(invalid):
					printGrid(grid)
					go = input(": ")
					if(not is_number(go)):
						go = 99
					go = int(go)
					if(1 <= go <= 7):
						for i in range(5, -1, -1):
							if(grid[i][go-1] == "*"):
								grid[i][go-1] = player
								invalid = False
								turncount += 1
								checkWon(grid)
								break
					else:
						printGrid(grid,"invalid input")
			else:
				# opponent's turn
				while(isItMyTurn() == False):
					pass
		printGrid(grid)
		if(finished == player):
			input("YOU WIN!\nPress enter to quit\n: ")
		else:
			input("YOU LOSE!\nPress enter to quit\n: ")



################
#              #
#    CLIENT    #
#              #
################

def isItMyTurn():
	global turncount
	global player
	#print("player", player)
	#print("turncount", turncount)
	
	if(turncount % 2 == 0):
		even = True
	else:
		even = False
		
	if(even and player == "X"):
		return True
	elif(not even and player == "O"):
		return True
	else:
		return False
	
def printGrid(grid, head = "", won = False):
	global player
	global opponent
	
	clear()
	
	myTurn = isItMyTurn()
	if(myTurn):
		whose = " YOUR TURN"
	else:
		whose = " OPPONENT'S TURN"
	print(head)
	if(not won):
		print("TURN: " + str(turncount) + whose)
	else:
		print("GAME OVER")
	print("YOU: " + player + "   OPPONENT: " + opponent)
	print("      1 2 3 4 5 6 7")
	for i in range(0,6):
		currentRow = "    | "
		for j in range(0,7):
			currentRow += grid[i][j] + " "
		currentRow += "|"
		print(currentRow)
	print()
	
	return myTurn

	

def clientGame():
	global finished
	global grid
	global turncount
	while(finished == "*"):
		
		
		if(printGrid(grid)):
			invalid = True
			while(invalid):
			# your turn
				printGrid(grid)
				go = input(": ")
				if(not is_number(go)):
					go = 99
				go = int(go)
				if(1 <= go <= 7):
					
					sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
					sock.connect((HOST, PORT))
					sock.sendall(pickle.dumps([1,go]))
					received = pickle.loads(sock.recv(1024))
					
					invalid = received[0]
					grid = received[1]
					turncount = received[2]
					
				else:
					printGrid(grid,"invalid input")
		else:
			# opponent's turn
			while(isItMyTurn() == False):
				time.sleep(.5)
				
				sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				sock.connect((HOST, PORT))
				sock.sendall(pickle.dumps([2]))
				received = pickle.loads(sock.recv(1024))
				
				turncount = received[0]
				grid = received[1]
				finished = received[2]
				sock.close()
			printGrid(grid)
			
	printGrid(grid)
	if(finished == player):
		input("YOU WIN!\nPress enter to quit\n: ")
	else:
		input("YOU LOSE!\nPress enter to quit\n: ")
	

def c4Client():
	global HOST
	global PORT
	global player
	global opponent
	global turnCount
	
	clear()
	HOST = input("Enter the IP that you want to connect to\n: ")
	clear()
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	try:
		sock.connect((HOST, PORT))
		toSend = [0]
		sock.sendall(pickle.dumps(toSend))
		received = pickle.loads(sock.recv(1024))
		player = received[0]
		print(player)
		if(player == "O"):
			opponent = "X"
		else:
			opponent = "O"
		
		
	except Exception as e:
		print("Failed to connect:\n ", e,"\n\nPress enter to return to menu")
		input(": ")
	else:
		clientGame()






if __name__ == "__main__":
	temp = 0
	while True:
		clear()
		if(temp == 0):
			choice = input("\nWhat would you like to do?\n (1) Host a game\n (2) Join a game\n (3) Quit\n: ")
		else:
			choice = input("Invalid choice\nWhat would you like to do?\n (1) Host a game\n (2) Join a game\n (3) Quit\n: ")
		temp = 1
		if(choice == "1"):
			c4Server()
			# it's too hard to stop the daemon so we just close the program :)
			sys.exit()
		elif(choice == "2"):
			c4Client()
			sys.exit()
		elif(choice == "3"):
			sys.exit()
		else:
			clear()
			