#!/usr/bin/python

import termios, sys, os

datestr="130910"

day=datestr[0:2]
month=datestr[2:4]
year=datestr[4:6]

#print 'argv len='+repr(len(sys.argv))
#print 'argv[1] ='+sys.argv[0]

if __name__ == '__main__':
		print 'datestr=' + str(datestr)
		print 'day=' + str(day)
		print 'month=' + str(month)
		print 'year=' + str(year)
