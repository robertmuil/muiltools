import pylab as pp
import numpy as np


s_uniform = [1,1,2,2,3,3] #uniform

assert(np.mean(s_uniform) == 2)
assert(np.var(s_uniform) == 4./6)
assert(np.std(s_uniform) == np.sqrt(4./6))

def test_random_processes_accumulating():
	orig_rand=np.random.rand(4,200000)+1.0
	aa=orig_rand - orig_rand[3]
	ca=np.cumsum(aa.T,axis=0)
	pp.figure(); pp.plot(ca)

	pp.figure(); pp.plot(100.0*ca/orig_rand[3:,:].T)

test_random_processes_accumulating()
