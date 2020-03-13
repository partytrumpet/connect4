import curses
import os
import sys

grid = [[" " for col in range(79)] for row in range(24)]

for i in range(0,len(grid)):
	grid[i][0] = "#"
	grid[i][-1] = "#"

for j in range(0,len(grid[0])):
	grid[0][j] = "#"
	grid[-1][j] = "#"

grid[11][3] = "O"
#print(grid)

def main(win):
	global grid
	win.nodelay(True)
	key=""
	win.clear()
	#win.addstr("Detected key:")

	for i in range(0,len(grid)):
		for j in range(0,len(grid[0])):
			win.addstr(grid[i][j])
		win.addstr("\n")
	while True:
		try:
			key = win.getch()
			#win.clear()
			if key == 3:
				sys.exit()
			if key == os.linesep:
				break
		except Exception as e:
			# No input
			print(e)

curses.wrapper(main)

#60x20
