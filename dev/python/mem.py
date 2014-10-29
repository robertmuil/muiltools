blah ='fesf'

def something ():
	global blah
	blah=[1,2,3]

	print str(blah) + ' <func'


print str(blah) + ' < global'

something()

print str(blah) + ' < global'
