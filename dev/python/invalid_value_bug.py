import cPickle

print 'loading data...'
iv = cPickle.load(open('invalid_value.pickle', 'r'))
print ' done: iv=%s.'%(str(iv))
print 'arithmetic on 1st element of array...'
#This will succeed:
iv[0]-1
print ' done.'

print 'arithmetic on array...'
#This will fail:
iv-1
print ' done.'
