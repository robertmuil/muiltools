import numpy as np
import pandas as pd
from scipy.special import logit
import matplotlib.pyplot as pp
#import seaborn

sample_size = 1000000

sample_norm = np.random.normal(size=sample_size)
sample_logit = logit(np.random.uniform(size=sample_size))
sample_cauchy = np.random.standard_cauchy(size=sample_size)
sample_uniform_wide = np.random.uniform(low=-10000,high=10000, size=sample_size)
bins = np.linspace(-100,100,100)
pp.ion()

pp.figure()
pp.subplot(2,1,1)
pp.hist(sample_norm, bins=bins,
		label='normal', log=True)
pp.hist(sample_logit, bins=bins, alpha=0.5,
		label='logit(uniform)')
pp.hist(sample_cauchy, bins=bins, alpha=0.5,
		label='cauchy')
pp.hist(sample_uniform_wide, bins=bins, alpha=0.5,
		label='uniform_wide')
pp.legend()

pp.subplot(2,1,2)
pp.plot(pd.expanding_mean(sample_norm), label='expanding mean of normal')
pp.plot(pd.expanding_mean(sample_logit), label='expanding mean of logit(uniform)')
pp.plot(pd.expanding_mean(sample_cauchy), label='expanding mean of cauchy')
pp.plot(pd.expanding_mean(sample_uniform_wide), label='expanding mean of uniform_wide')
pp.ylim(-3,3)
pp.legend()
pp.show()


