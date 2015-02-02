import pylab as pp
import numpy as np
import sys
from scipy.stats import pearsonr
import ipdb
import itertools
import seaborn

dbg_lvl=0

def dbg(lvl,thestr):
	if lvl<=dbg_lvl:
		print 'D%d: %s'%(lvl,thestr)

def gen_data(n, d, R, ranges=None):
	"""
	just generates random data with the given parameters:
	 n = number of data points
	 d = dimensions
	 R = desired fraction of correlated versus noise, of size d-1
	 ranges = list of d tuples containing the range of each variable
	"""

	if ranges is not None:
		assert(len(ranges)==d)
	
	assert(len(R)==(d-1))

	R = np.array(R)

	#create the IVs - create row for DV also, to be overwritten
	D = np.random.randn(n, d)

	#create the DV dependent on the correlation coefficients
	correlated_portion = (R * D[:,1:]).mean(1)
	random_portion = ((1-R).mean() * D[:,0])
	D[:,0] = (correlated_portion + random_portion)

	if dbg_lvl >0:
		ipdb.set_trace()
	return D

def get_slope(P0,P1):
	"""

	>>> get_slope((0,0),(1,1))
	1.0
	>>> get_slope((0,0),(1,2))
	2.0
	>>> get_slope((0,0),(2,1))
	0.5
	>>> get_slope((0,0),(3,3))
	1.0

	"""
	dX=float(P1[0])-float(P0[0])
	dY=float(P1[1])-float(P0[1])
	return dY/dX

	
def ols(D):
	"""
	Given a matrix of values in which the first variable is taken to be
	the dependent variable, will return the ordinary least squares fit.

	This regression line is defined as the line with the minimum squared
	vertical distances between line and data points.

	return is [m, c] where m is slope and c is intercept
	"""
	pass

def thiel_sen(D):
	"""
	Given a matrix of values in which the first variable is taken to be the dependent variable,
	will return the Theil-Sen regression line.

	This line is defined as the median of the slopes of the lines between all pairs of data points.

	returns:
		[m, c] where m is slope and c is intercept
	"""

	#get all pairs
	pair_iter = itertools.permutations(D,2)

	#compute slope for each
	slopes=np.ones(D.shape[0]*(D.shape[0]-1))*np.nan
	for idx,pair in enumerate(pair_iter):
		slopes[idx]=get_slope(pair[0],pair[1])
	
	#compute median
	m = np.median(slopes)
	return (m,)

def test_thiel_sen():

	d = 2
	desired_coefficient=0.5
	if len(sys.argv)>1:
		desired_coefficient=float(sys.argv[1])


	D = gen_data(100, d, [desired_coefficient]*(d-1), ((0.0,10.0),(0.0,10.0)))

	(pR,pP) = pearsonr(D[:,0], D[:,1])
	(tsM,) = thiel_sen(D)
	print "Pearson's R=%.2f, P=%.2f"%(pR,pP)
	print "Thiel-Sen's M=%.2f"%(tsM)

	pp.figure();
	pp.plot(D[:,0], D[:,1:],'.',
			label='data')
	x=[min(D[:,0]), max(D[:,0])]
	y=tsM*x
	pp.plot(x,y,'r',
			label='Thiel-Sen Regression Line')
	pp.legend()
	pp.show()

def test_log_log_reg():

	x=np.linspace(0.01, 10, 1000)

	pp.figure()

	for w in [0.1,0.5,1.0,1.5,2.0,2.5,3.0]:
		#log(y) = w*log(x)
		y=np.exp(w*np.log(x))
		[line1] = pp.plot(x,y, label='log(y) = {:.1f} * log(x) (i.e. y = x^{:.1f})'.format(w,w))

		if False:
			y2=x**w
			pp.plot(x,y2, '.', color=line1.get_color(), label='y=x^{:.1f}'.format(w))
	
	pp.xlabel('x')
	pp.ylabel('y')
	pp.ylim(0,20)
	pp.legend()
	pp.title('Linear models that were fit in the log-log space.')
	pp.show()

if __name__ == '__main__':

	if False:
		test_thiel_sen()

	if True:
		test_log_log_reg()
