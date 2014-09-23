#!/usr/bin/env python
# This was found to be failing on 2013/08/08, with following versions:
#Python 2.7.5
#numpy 1.7.1
#numpy.ma 1.0
#cPickle 1.71

import cPickle

fname='array_repr_failing.pkl'
print 'loading from "%s"'%fname
aa=cPickle.load(open(fname, 'rb'))
print 'loaded: type(aa)=%s, aa.dtype=%s, shape(aa)=%s'%(str(type(aa)), str(aa.dtype), str(aa.shape))
print ' -> type(aa[0])=%s, aa[0].dtype=%s, shape(aa[0])=%s' % (str(type(aa[0])), str(aa[0].dtype), str(aa[0].shape))
print ' -> str(aa[0])=%s\n -> repr(aa[0])=\n%s' % (str(aa[0]), repr(aa[0]))
print ' -> type(aa[1])=%s, aa[1].dtype=%s, shape(aa[1])=%s' % (str(type(aa[1])), str(aa[1].dtype), str(aa[1].shape))
print ' -> str(aa[1])=%s\n -> repr(aa[1])=\n%s' % (str(aa[1]), repr(aa[1]))
print 'attempting repr(aa):'
repr(aa)
