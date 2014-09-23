import numpy as np
import warnings

np.seterr(all='raise')

print 'numpy version = %s'  % np.__version__
print 'numpy.geterr() = %s' % np.geterr()
print 'warnings.filters:'
print warnings.filters

counter=0
aa = 0
while True:
	aa - 1
	bb = np.ma.empty(200)
	bb - 1
	aa=bb
	#aa[190:200] = np.arange(10)
	counter+=1
	if (counter % 10000) == 0:
		print '%d iters'%counter
