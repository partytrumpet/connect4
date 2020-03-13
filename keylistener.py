import curses
import os

grid = [[" " for col in range(60)] for row in range(20)]
for i in range(0,len(grid)):
	grid[0][i] = "#"
	grid[-1][i] = "#"

for j in range(0,len(grid)):
	grid[j][0] = "#"
	grid[j][-1] = "#"

print(grid)

def main(win):
    win.nodelay(True)
    key=""
    win.clear()
    win.addstr("Detected key:")
    while True:
        try:
           key = win.getch()
           win.clear()
           win.addstr("Detected key:")
           win.addstr(str(key))
		   if key == 3:
			   sys.exit()
           if key == os.linesep:
              break
        except Exception as e:
           # No input
           print(e)

curses.wrapper(main)

#60x20
