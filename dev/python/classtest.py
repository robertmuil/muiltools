class a(object):
	def __init__(self):
		print 'a.__init__()'

class b(a):
	def __init__(self):
		print 'b.__init__()'
		super(b, self).__init__()

#mya = a()
#myb = b()
