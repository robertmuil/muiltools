import numpy as np
yee=1
bla=[1,2,3]
ble=np.array([1,2,3])

def inochange():
	yee=-1

def ichange():
	global yee
	print 'local yee='+str(yee)
	yee=-2

def say_hello(yee=None, bla=None, ble=None):
	print 'local scope: yee='+str(yee)
	print 'local scope: bla='+str(bla)
	print 'local scope: ble='+str(ble)
	yee=99
	bla[0]=99
	print 'local scope: yee='+str(yee)
	print 'local scope: bla='+str(bla)
	print 'local scope: ble='+str(ble)

print 'global scope: yee='+str(yee)
print 'global scope: bla='+str(bla)
print 'global scope: ble='+str(ble)
print 'say_hello()...',
say_hello(yee,bla)
print '...done'
print 'global scope: yee='+str(yee)
print 'global scope: bla='+str(bla)
print 'global scope: ble='+str(ble)
print 'inochange()...',
inochange()
print '...done'
print 'global scope: yee='+str(yee)
print 'global scope: bla='+str(bla)
print 'global scope: ble='+str(ble)
yee=2
print 'global scope: yee='+str(yee)
print 'ichange()...',
ichange()
print '...done'
print 'global scope: yee='+str(yee)
print 'global scope: bla='+str(bla)
print 'global scope: ble='+str(ble)

print '-----'

