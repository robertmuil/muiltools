#!/usr/bin/env python

class StreamTee:
    
	"""Intercept a stream.
	Invoke like so:
	sys.stdout = StreamTee(sys.stdout)
	See: grid 109 for notes on older version (StdoutTee).
	http://wiki.python.org/moin/PrintFails
	"""
    
	def __init__(self, target):
		self.target = target

	def write(self, s):
		s = self.intercept(s)
		self.target.write(s)

	def intercept(self, s):
		"""Pass-through -- Overload this."""
		return s

class SafeStreamFilter(StreamTee):
	"""Convert stream traffic to something safe."""
	def __init__(self, target):
		StreamTee.__init__(self, target)
		self.encoding = 'UTF-8'
		self.errors = 'replace'
		self.encode_to = self.target.encoding
	def intercept(self, s):
		return s.encode(self.encode_to, self.errors)

def console_mode():
	"""Console mode."""
	import sys
	sys.stdout = SafeStreamFilter(sys.stdout)

import locale
import sys

prefenc = locale.getpreferredencoding()

print 'prefenc='+str(prefenc)
outenc = sys.stdout.encoding
print 'stdoutenc='+str(outenc)

print 'console'
console_mode()
outenc = sys.stdout.encoding
print 'stdoutenc='+str(outenc)

uu = u'abc_\u03a3_d'

print uu
