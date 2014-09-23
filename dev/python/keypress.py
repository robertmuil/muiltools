#!/usr/bin/python

import termios, sys, os

print 'argv len='+repr(len(sys.argv))
print 'argv[1] ='+sys.argv[0]

TERMIOS = termios
def getkey():
	fd = sys.stdin.fileno()
	old = termios.tcgetattr(fd)
	new = termios.tcgetattr(fd)
	new[3] = new[3] & ~TERMIOS.ICANON & ~TERMIOS.ECHO
	new[6][TERMIOS.VMIN] = 1
	new[6][TERMIOS.VTIME] = 0
	termios.tcsetattr(fd, TERMIOS.TCSANOW, new)
	c = None
	try:
		c = os.read(fd, 1)
	finally:
		termios.tcsetattr(fd, TERMIOS.TCSAFLUSH, old)
	return c

if __name__ == '__main__':
	print 'type something'
	s = ''
	while 1:
		c = getkey()
		if c == '\n':     ## break on Return/Enter
			break
		print 'got', c
		s = s + c
	print s
