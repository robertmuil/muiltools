'''
Created on Jan 11, 2012

@author: rmuil
'''

import numpy as np
import pylab as pl
from copy import deepcopy

xx = np.zeros(1000)
#xx[100:200]=1.0
xx[300:700]=np.sin(np.arange(400)/40.0)

delta = np.zeros(200)
delta[0] = 1.0

echofunc = np.zeros(200)
echofunc[199] = 0.6

impulse =np.convolve(xx, delta, 'full')
echoresponse =np.convolve(xx, echofunc, 'full')

fig = pl.figure()

xline = pl.plot(xx, 'bx-')
efline = pl.plot(echofunc, 'yx-')
dline = pl.plot(delta, 'rx-')
iline = pl.plot(impulse, 'ro')
erline = pl.plot(echoresponse, 'yo')

pl.legend(['input',
		'shift function',
		'delta function',
		'impulse response',
		'shift response',
])

pl.ylim((-1, 2))
pl.xlim((-10, 1010))


pl.show()