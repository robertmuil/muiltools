import numpy as np
import pandas as pd
import timeit

arr=np.zeros((10, 5))
a = pd.DataFrame(arr, columns=('a','b','c','d','e'))

print a

a.loc[0,0:3] = 1,2,3

print a
