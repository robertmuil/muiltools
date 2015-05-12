from __future__ import print_function
import numpy as np
import statsmodels.api as sm
import statsmodels.formula.api as sf
from scipy import stats

def dbg(msg):
	print('D|{}'.format(msg))

def random_binary_sequence(nsample,p_transition=0.01):
	"""
	just a binary sequence of nsample points with a transition in state
	at every point with probability p_transition
	default is 1% chance of transition
	>>> str(random_binary_sequence(5, 1.0).astype(int))
	'[1 0 1 0 1]'
	>>> np.random.seed(123456)
	>>> str(random_binary_sequence(5, 0.5).astype(int))
	'[1 1 0 0 1]'
	>>> str(random_binary_sequence(10, 0.2).astype(int))
	'[0 0 0 1 1 1 1  0 0 0]'
	"""
	mask = np.ones(nsample).astype(bool)
	seq = np.zeros(nsample).astype(bool)
	transitions = np.random.random_sample(nsample)<p_transition

	for tr in np.where(transitions)[0]:
		mask[0:tr]=False
		seq ^= mask

	return seq

if __name__ == '__main__':
	do_plot = True
	do_linear = False
	do_log = True

	nsample = 5000
	sig = 00.5

	if True:
		x1 = np.linspace(0, 20, nsample)
		x2 = np.sin(x1)
		x3 = (x1-5)**2
		xb = random_binary_sequence(nsample, 5.0/nsample).astype(int)
		X = np.column_stack((x1, x2, x3, xb))
		X = sm.add_constant(X)
		beta = [5., 0.5, 0.5, -0.02, 0.0]
		y_true = np.dot(X, beta)

		y = y_true + sig * np.random.normal(size=nsample)

		data = {"x1" : x1, "xb": xb, "y" : y}

		if do_log:
			log=np.log
			olsmod = sf.ols("log(y) ~ log(x1+1) + log(np.sin(x1)+1) + log(I((x1-5)**2)+1)", data=data)
		else:
			olsmod = sf.ols("y ~ x1 + np.sin(x1) + I((x1-5)**2) + xb", data=data)
		olsres = olsmod.fit()
		print(olsres.summary())
		ypred = olsres.predict(exog=data)
		residual = y-ypred

		(R,P) = stats.pearsonr(y,x1)
		print('y vs x1: {:.4f}, {:.4f}'.format(R,P))
		(R,P) = stats.pearsonr(y,x2)
		print('y vs x2: {:.4f}, {:.4f}'.format(R,P))
		(R,P) = stats.pearsonr(y,x3)
		print('y vs x3: {:.4f}, {:.4f}'.format(R,P))
		(R,P) = stats.pearsonr(y,xb)
		print('y vs xb: {:.4f}, {:.4f}'.format(R,P))
		(R,P) = stats.pearsonr(residual,x1)
		print('residual vs x1: {:.4f}, {:.4f}'.format(R,P))
		(R,P) = stats.pearsonr(residual,x2)
		print('residual vs x2: {:.4f}, {:.4f}'.format(R,P))
		(R,P) = stats.pearsonr(residual,x3)
		print('residual vs x3: {:.4f}, {:.4f}'.format(R,P))
		(R,P) = stats.pearsonr(residual,xb)
		print('residual vs xb: {:.4f}, {:.4f}'.format(R,P))

		x1n = np.linspace(20.5,25, nsample//10.0)
		xbn = np.zeros(x1n.shape)
		Xnew = np.column_stack((np.ones(x1n.shape), x1n, np.sin(x1n), (x1n-5)**2, xbn))
		#Xnew = sm.add_constant(Xnew)
		#ynewpred =  olsres.predict(Xnew) # predict out of sample
		ynewpred = olsres.predict(exog=dict(x1=x1n, xb=xbn))

		if do_plot:
			import matplotlib.pyplot as plt

			fig, ax = plt.subplots()
			ax.plot(x1, y, 'o', alpha=0.2, label="Data")
			ax.plot(x1, y_true, 'b-', label="True")
			ax.plot(np.hstack((x1, x1n)), np.hstack((ypred, ynewpred)), 'r', label="OLS prediction")
			ax.legend(loc="best");

			fig2,(ax_res1, ax_res2, ax_res3, ax_res4) = plt.subplots(1,4)
			ax_res1.plot(x1, residual, '.', label='x1')
			ax_res1.set_xlabel('x1')
			ax_res1.set_ylabel('residual y')
			ax_res2.plot(np.sin(x1), residual, '.', label='sin(x1)')
			ax_res2.set_xlabel('sin(x1)')
			ax_res2.set_ylabel('residual y')
			ax_res3.plot((x1-5)**2, residual, '.', label='(x1-5)**2')
			ax_res3.set_xlabel('(x1-5)**2')
			ax_res3.set_ylabel('residual y')
			ax_res4.plot(xb, residual, '.', label='xb')
			ax_res4.set_xlabel('xb')
			ax_res4.set_ylabel('residual y')


	if do_plot:
		plt.show()
