#!env python2
#Author: Robert Muil
import subprocess as sp
import string
import sys

def find_arguments(prog):
	valid_args = {}
	for arg in string.lowercase + string.uppercase:
		try:
			output = sp.check_output([prog,"-"+arg], stderr=sp.STDOUT)
			valid_args[arg] = output
			#print 'output=['+output+']'
		except sp.CalledProcessError:
			pass
			
	return valid_args

if __name__ == '__main__':
	print 'valid arguments: ' + str(find_arguments(sys.argv[1]).keys())
