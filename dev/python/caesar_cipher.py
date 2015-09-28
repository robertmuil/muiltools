import string

uc = string.ascii_uppercase
caesar = ''.join([uc[(uc.index(c)+3)%luc] for c in uc])
caesar_table = string.maketrans(uc, caesar)
luc = len(uc)

lazydog = 'THE QUICK BROWN FOX JUMPS OVER THE LAZY DOG'

def caesarcipher(istr=lazydog):
	ostr = istr.translate(caesar_table)
	return ostr

if __name__ == '__main__':
	print 'in:  '+lazydog
	print 'out: '+caesarcipher(lazydog)
