import numpy as np
yee=1
bla=[1,2,3]
ble=np.array([1,2,3])

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
say_hello(yee,bla)
print 'global scope: yee='+str(yee)
print 'global scope: bla='+str(bla)
print 'global scope: ble='+str(ble)

print '-----'

