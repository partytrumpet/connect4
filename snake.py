import curses
import os
import sys

grid = [[" " for col in range(24)] for row in range(79)]
playerX = 3
playerY = 11
playerIcon = "O"
for i in range(0,len(grid)):
	grid[i][0] = "#"
	grid[i][-1] = "#"

for j in range(0,len(grid[0])):
	grid[0][j] = "#"
	grid[-1][j] = "#"

grid[playerX][playerY] = playerIcon
#print(grid)

def main(win):
	global grid
	global playerX
	global playerY
	global playerIcon
	win.nodelay(False)
	key=""
	win.clear()
	#win.addstr("Detected key:")
	grid[playerX][playerY] = playerIcon
	# rows
	for i in range(0,len(grid[0])):
		# cols
		for j in range(0,len(grid)):
			win.addstr(grid[j][i])
		win.addstr("\n")
	while True:
		try:
			key = win.getch()
			win.clear()

			if key == 3:
				sys.exit()
			# up/w
			if key == 119 or key == 259:
				if not grid[playerX][playerY-1]=="#":
					grid[playerX][playerY] = " "
					playerY -= 1
					grid[playerX][playerY] = playerIcon

			# right/d
			if key == 100 or key == 261:
				if not grid[playerX+1][playerY]=="#":
					grid[playerX][playerY] = " "
					playerX += 1
					grid[playerX][playerY] = playerIcon

			# down/s
			if key == 115 or key == 258:
				if not grid[playerX][playerY+1]=="#":
					grid[playerX][playerY] = " "
					playerY += 1
					grid[playerX][playerY] = playerIcon

			# left/a
			if key == 97 or key == 260:
				if not grid[playerX-1][playerY]=="#":
					grid[playerX][playerY] = " "
					playerX -= 1
					grid[playerX][playerY] = playerIcon

			for i in range(0,len(grid[0])):
				# cols
				for j in range(0,len(grid)):
					win.addstr(grid[j][i])
				win.addstr("\n")
			if key == os.linesep:
				break
		except Exception as e:
			# No input
			print(e)

curses.wrapper(main)

#60x20
