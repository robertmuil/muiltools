"""
This is simply an exploration of several distributions that behave somewhat
counter-intuitively: the Cauchy distribution being the most interesting - a
distribution that arises in the ratio of normal distributions, and which does
not itself have a defined mean - meaning that no matter how many data points
you collect in your sample, you're no better off predicting the next point.
Means over massive samples of a Cauchy distribution can still exhibit step-
changes with a single new data point.

This may not seem practically relevant, except in situations where ratios are
being hypothesis tested. Things such as return ratio way well exhibit such
badly defined behaviour under certain circumstances. So far as I can see,
the circumstances are:
 - the denominator of the tested metric is distributed around 0
     How would this be the case? I think that if we are looking at return rates
		 between two groups - so a difference of return rates, we may well find
		 this sort of bad behaviour.
"""
import numpy as np
import pandas as pd
from scipy.special import logit
import matplotlib.pyplot as pp
import seaborn

sample_size = 100000

pp.ion()

dists = pd.DataFrame(np.random.normal(size=sample_size), columns=['normal'])
dists['inverse_normal'] = 1/(np.random.normal(size=sample_size))
dists['normal_ratio'] = np.random.normal(size=sample_size)/(np.random.normal(size=sample_size))
dists['poisson'] = (np.random.poisson(size=sample_size))
dists['poisson_ratio'] = (np.random.poisson(size=sample_size))/(np.random.poisson(size=sample_size))
dists['poisson_diff'] = (np.random.poisson(size=sample_size))-(np.random.poisson(size=sample_size))
dists['logit'] = logit(np.random.uniform(size=sample_size))
dists['cauchy'] = np.random.standard_cauchy(size=sample_size)
dists['uniform_wide'] = np.random.uniform(low=-100,high=100, size=sample_size)
bins = np.linspace(-100,100,100)

dists.hist(bins=bins, log=True, alpha=0.5)

pd.expanding_mean(dists).plot()
pp.title('Expanding Means')
pp.ylim(-3,3)
pp.show()


