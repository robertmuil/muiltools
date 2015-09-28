import pandas as pd
import matplotlib.pyplot as pp
import numpy as np

ix3 = pd.MultiIndex.from_arrays([['a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c', 'a', 'b', 'c'], ['bar', 'bar', 'bar', 'foo', 'foo', 'foo', 'goo', 'goo', 'goo', 'hoo', 'hoo', 'hoo']], names=['letter', 'word'])
df = pd.DataFrame({'errlo': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12], 'errhi': [40, 38, 36, 34, 32, 30, 28, 26, 24, 22, 20, 18]}, index=ix3)
df['mean']=df.mean(axis='columns')
data=df.unstack(level='letter')

print data

if True:
	print '1st approach'
	errlo     = data['mean'] - data['errlo']
	errhi     = data['errhi'] - data['mean']
	errlo_arr = errlo.values[:,np.newaxis,:]
	errhi_arr = errhi.values[:,np.newaxis,:]
	yerr      = np.append(errlo_arr, errhi_arr, axis=1).T
	data['mean'].plot(kind='bar', yerr=yerr)
	pp.title('1st approach')
	pp.show()

if True:
	print '2nd approach'
	dfci = df[['errlo','errhi','mean']].copy()
	dfci['errlo']  = dfci['mean'] - dfci['errlo']
	dfci['errhi']  = dfci['errhi'] - dfci['mean']

	dfci=dfci.unstack(level='letter')

	dfci['mean'].plot(kind='bar', yerr=dfci[['errlo','errhi']].T.values)
	pp.title('2nd approach')
	pp.show()

if True:
	print '3rd approach'
	dfci = data[['errlo','errhi','mean']].copy()
	dfci['errlo']  = dfci['mean'] - dfci['errlo']
	dfci['errhi']  = dfci['errhi'] - dfci['mean']

	#dfci=dfci.unstack(level='letter')

	dfci['mean'].plot(kind='bar', yerr=dfci[['errlo','errhi']].T.values)
	pp.title('3rd approach')
	pp.show()
