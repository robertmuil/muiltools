
#to maintain the original exception (including the line pointer and traceback)

blah=[1,2,3]

try:
	blah[4]
except IndexError as exc:
	args = exc.args
	if args is None:
		args = []
	else:
		args = list(args)
	args[0] = 'No such element in "{}"'.format("something")
	exc.args = tuple(args)
	raise
