import pandas

print '=== Original Bug #2770 ==='
x = pandas.DataFrame([['deleteMe',1, 9],['keepMe',2, 9],['keepMeToo',3, 9]], columns=['first','second', 'third'])
print '\n * create df:'
print x
x = x.set_index(['first','second'], drop=False)
print '\n * set index:'
print x

x = x[x['first'] != 'deleteMe'] 
print '\n * Chop off all the \'deleteMe\' rows:'
print x

print '\n * index:'
print x.index 
print "#Good: Index no longer has any rows with 'deleteMe'. But...."

print '\n * index.levels:'
print x.index.levels
print "#Bad: index still shows the 'deleteMe' values are there. But why? We deleted them."

print '\n * groupby:'
print x.groupby(level='first').sum()
print "#Bad: it's creating a dummy row for the rows we deleted!"

print '=== Additional Problem: unique values ==='
x = pandas.DataFrame([['deleteMe',1, 9],['keepMe',2, 9],['keepMeToo',3, 9]], columns=['first','second', 'third'])

x = x.set_index(['first','second'], drop=False)

print 'determine unique from levels:'
print len(x.index.levels[0])
print 'determine unique from time-consuming unique() call:'
print len(x.index.get_level_values(level='first').unique())
