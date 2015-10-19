def a_func(a_list=None):
	if a_list is not None:
		a_list += ['haha!']

mylist=['start']

print mylist

a_func(mylist)

print mylist
