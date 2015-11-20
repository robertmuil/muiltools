import numpy as np

categories={
		'first': [1],
		'low':   [2,3,4],
		'mid':   [5,6,7],
		'hi':    [8,9]
		}

def categorise(a,categories=categories):
	"""simple binning"""
	for c,v in categories.iteritems():
		if a in v:
			return c

	return None

for ii in range(11):
	print ii,' - ',categorise(ii)

vcategorise = np.vectorize(categorise, excluded=['categories'])

data = np.array(range(11))

print vcategorise.__doc__
print vcategorise(data)
print vcategorise(range(11))

