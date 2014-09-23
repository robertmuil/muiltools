#!/usr/bin/python

import termios, sys, os

maxLatDiff=1000
maxLonDiff=10000
blah=0

#print 'argv len='+repr(len(sys.argv))
#print 'argv[1] ='+sys.argv[0]

date="211010"
day=date[-6:-4]
month=date[-4:-2]
year=date[-2:]
print 'day='+day
print 'month='+month
print 'year='+year


if __name__ == '__main__':
	lat=8000
	prevLat=None
	lon=52001
	prevLon=None
	if blah==None:
		print 'blah is none'
	if (((prevLat != None) and (abs(lat-prevLat)>maxLatDiff))) or ((prevLon != None) and (abs(lon-prevLon)>maxLonDiff)):
		print 'bupow, problem!'
	else:
		print 'alles gut'
