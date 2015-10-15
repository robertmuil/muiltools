"""
This shows the phenomenon (feature?) in python that default arguments are
stored as global variables. This means that if one alters the default argument,
these alterations are preserved - so every subsequent call to the function that
does not set that argument explicitly will use the updated default argument.

This only affects non-primitive objects: if it's just an int, this doesn't hold,
but lists, dicts, etc. are all affected.
"""

def blah(a,kwargs=[]):
	kwargs.append(a)
	print kwargs


blah(1)
#This shows problem:
blah(2)

blah(3,[])
#and here it is again:
blah(4)
