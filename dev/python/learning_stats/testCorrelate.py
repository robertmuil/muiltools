import scipy, pylab
import scipy.optimize
from numpy import argmax

# make x data
num = 100
x = scipy.linspace(-10, 10, num=num)
distancePerLag = x[1]-x[0]

# make two gaussians, with different means
offset = 2.0
y1 = scipy.exp(-x**2/8.0)
y2 = scipy.exp(-(x-offset)**2/1.0)

# compute the cross-correlation between y1 and y2
ycorr = scipy.correlate(y1, y2, mode='full')
xcorr = scipy.linspace(0, len(ycorr)-1, num=len(ycorr))

# define a gaussian fitting function where
# p[0] = amplitude
# p[1] = mean
# p[2] = sigma
fitfunc = lambda p, x: p[0]*scipy.exp(-(x-p[1])**2/(2.0*p[2]**2))
errfunc = lambda p, x, y: fitfunc(p,x)-y

# guess some fit parameters
p0 = scipy.c_[max(ycorr), scipy.where(ycorr==max(ycorr))[0], 5]
# fit a gaussian to the correlation function
p1, success = scipy.optimize.leastsq(errfunc, p0.copy()[0],
                                     args=(xcorr,ycorr))
# compute the best fit function from the best fit parameters
corrfit = fitfunc(p1, xcorr)

# get the mean of the cross-correlation
xcorrMean = p1[1]

# convert index to lag steps
# the first point has index=0 but the largest (negative) lag
# there is a simple mapping between index and lag
nLags = xcorrMean-(len(y1)-1)

# convert nLags to a physical quantity
# note the minus sign to ensure that the
# offset is positive for y2 is shifted to the right of y1
# a negative offset means that y2 is shifted to the left of y1
# I don't know what the standard notation is (if there is one)
offsetComputed = -nLags*distancePerLag

# see how well you have done by comparing the actual
# to the computed offset
print 'xcorrMean, nLags = ', \
     xcorrMean, ', ', nLags
print 'actualOffset, computedOffset = ', offset,', ', offsetComputed

# visualize the data
# plot the initial functions
pylab.subplot(211)
pylab.plot(x, y1, 'ro')
pylab.plot([x[argmax(y1)], x[argmax(y1)]], [0, max(y1)], 'g-')
pylab.plot(x, y2, 'bo')
pylab.plot([x[argmax(y2)], x[argmax(y2)]], [0, max(y2)], 'g-')

# plot the correlation and fit to the correlation
pylab.subplot(212)
pylab.plot(xcorr, ycorr, 'k.')
pylab.plot(xcorr, corrfit, 'r-')
pylab.plot([xcorrMean, xcorrMean], [0, max(ycorr)], 'g-')
pylab.show()
