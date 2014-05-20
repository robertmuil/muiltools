#!/usr/bin/env python2
#Author: Robert Muil
# A helper to parse the 'einzelne verbindungen' from an o2 invoice (rechnung)
# Steps:
# - open EVN pdf in acrobat
# - copy SMS tables into a txt file
# - copy Phone call tables into a txt file
# - run this over the text files
import sys
import numpy as np
import re
import logging
from logging import log
import os

dbg_lvl=0

def usage():
	print """ call this with a single text file as input. output will go to stdout """

def dbg(lvl, the_str):
	if lvl <= dbg_lvl:
		print "D%d: %s"%(lvl,the_str)

if len(sys.argv) < 2:
	usage()
	sys.exit(1)

fname = sys.argv[1]

dbg(1,"parsing '%s'"%(fname))

rechnung_type = 'call'
if ('sms' in fname.lower()) or ('msg' in fname.lower()) or ('message' in fname.lower()):
	rechnung_type = 'msg'

if rechnung_type not in ['msg']:#, 'call']:
	raise NotImplementedError('parsing of %s coming soon promise'%(rechnung_type))

rawdata = np.genfromtxt(fname, 
		dtype=None,
		delimiter=[10,1,8,1,999],#' 0', ' '],
		names=['date','_space', 'time', '_space2','details'],
		usecols=[0,2,4],
		skip_header=1)

data = np.zeros(rawdata.shape[-1], dtype={'names':['date', 'time', 'type', 'number', 'price','price_to_pay', 'notes'], 'formats':['S10', 'S8', 'S999','S200', 'f8','f8','S999']})

detail_re = re.compile('(.*)\s([0-9]{3,})\s(?:(?:\(([0-9,]+)\)(.))|([0-9,]+))$')

data['date'] = rawdata['date']
data['time'] = rawdata['time']

lc = 0
valid_entries = 0
for dat in rawdata:

	mm = detail_re.match(dat['details'])

	dbg(2, 'line %d: '%(lc) + ('matches' if mm else 'DOES NOT MATCH'))

	if not mm:
		log(logging.WARNING, 'Line %d ("%s") does not match regular expression.'%(lc, dat))
	else:
		dbg(3, ' -> groups: %s' % (str(mm.groups())))
		
		data['type'][lc] = mm.group(1)
		data['number'][lc] = mm.group(2)
		covered = mm.group(4)
		if covered is not None:
			data['notes'][lc] = covered
		price = mm.group(5 if covered is None else 3)
		price = float(price.replace(',','.'))

		data['price'][lc] = price
		data['price_to_pay'][lc] = price if covered is None else 0

		valid_entries += 1

		dbg(3, ' -> data = %s' %(data[lc]))
	lc+=1

# Give some statistics out:
stat_str  = 'number of %ss:       %d%s\n'%(rechnung_type, valid_entries, ' (%d invalid entries)'%(data.shape[-1]-valid_entries) if (valid_entries != data.shape[-1]) else '')
stat_str += 'total price:        %s\n'%(data['price'].sum())
stat_str += 'total price to pay: %s'%(data['price_to_pay'].sum())

print stat_str

ofname = fname.rsplit('.',1)[0] + '-parsed.csv'

if os.path.exists(ofname):
	log(logging.WARNING, "'%s' exists already, not saving parsed output." % ofname)
else:
	np.savetxt(ofname, data, delimiter=',',
		header=stat_str+'\n\n'+','.join(data.dtype.names),
		fmt=['%s','%s','%s','%s','%.4f','%.4f','%s'])

	print ''
	print 'parsed output saved to %s'%(ofname)
