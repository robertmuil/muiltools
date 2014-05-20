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
import datetime
import ipdb

dbg_lvl=3

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

if rechnung_type == 'msg':
	detail_re = re.compile('(.*)\s([0-9]{3,})\s(?:(?:\(([0-9,]+)\)(.))|([0-9,]+))$')
	type_grp = 1
	number_grp = 2
	duration_grp = -1 #no duration for msgs
	covered_price_grp = 3
	covered_note_grp = 4
	price_to_pay_grp = 5

elif rechnung_type == 'call':
	detail_re = re.compile('([^\s]+\s)?([0-9]{3,})(?:\s([0-9]{2}:[0-9]{2}:[0-9]{2}))?\s(?:(?:\(([0-9,]+)\)(.))|([0-9,]+))$')
	type_grp = 1
	number_grp = 2
	duration_grp = 3
	covered_price_grp = 4
	covered_note_grp = 5
	price_to_pay_grp = 6

else:
	raise NotImplementedError('parsing of %s coming soon promise'%(rechnung_type))

rawdata = np.genfromtxt(fname, 
		dtype=None,
		delimiter= [    10,       1,      8,         1,      999],
		names=     ['date','_space', 'time', '_space2','details'], 
		usecols=[0,2,4],
		skip_header=1)

data = np.zeros(rawdata.shape[-1], dtype={'names':['date', 'time', 'duration', 'type', 'number', 'price','price_to_pay', 'notes'], 'formats':['S10', 'S8', 'i8', 'S999','S200', 'f8','f8','S999']})

data['date'] = rawdata['date']
data['time'] = rawdata['time']

lc = 0
valid_entries = 0
for dat in rawdata:

	mm = detail_re.match(dat['details'])

	dbg(2, 'line %d: '%(lc) + ('matches' if mm else 'DOES NOT MATCH'))

	if not mm:
		log(logging.WARNING, 'Line %d ("%s") does not match regular expression.'%(lc, dat))
		if dbg_lvl > 0:
			ipdb.set_trace()
	else:
		dbg(3, ' -> groups: %s' % (str(mm.groups())))
		
		data['type'][lc] = mm.group(type_grp)
		data['number'][lc] = mm.group(number_grp)
		covered = mm.group(covered_note_grp)
		if covered is not None:
			data['notes'][lc] = covered
		price = mm.group(price_to_pay_grp if covered is None else covered_price_grp)
		price = float(price.replace(',','.'))

		data['price'][lc] = price
		data['price_to_pay'][lc] = price if covered is None else 0

		if (duration_grp > 0) and (mm.group(duration_grp) is not None):
			tt = datetime.datetime.strptime(mm.group(duration_grp), '%H:%M:%S')
			dur = datetime.timedelta(hours=tt.hour, minutes=tt.minute, seconds=tt.second)
			data['duration'][lc] = dur.total_seconds()

		valid_entries += 1

		dbg(3, ' -> data = %s' %(data[lc]))
	lc+=1

# Give some statistics out:
stat_str  = 'number of %ss:       %d%s\n'%(rechnung_type, valid_entries, ' (%d invalid entries)'%(data.shape[-1]-valid_entries) if (valid_entries != data.shape[-1]) else '')
stat_str += 'total price:        %s\n'%(data['price'].sum())
stat_str += 'total price to pay: %s\n'%(data['price_to_pay'].sum())
if rechnung_type == 'call':
	td = datetime.timedelta(seconds=data['duration'].sum())
	td_charged = datetime.timedelta(seconds=data['duration'][data['price_to_pay']>0].sum())
	td_uncharged = datetime.timedelta(seconds=data['duration'][data['price_to_pay']==0].sum())
	stat_str += 'total duration:   %s (%d seconds)\n'%(str(td),td.total_seconds())
	stat_str += 'duration covered:   %s (%d seconds)\n'%(str(td_uncharged),td_uncharged.total_seconds())
	stat_str += 'duration charged:   %s (%d seconds)\n'%(str(td_charged),td_charged.total_seconds())

print stat_str

ofname = fname.rsplit('.',1)[0] + '-parsed.csv'

if os.path.exists(ofname):
	log(logging.WARNING, "'%s' exists already, not saving parsed output." % ofname)
else:
	np.savetxt(ofname, data, delimiter=',',
		header=stat_str+'\n'+','.join(data.dtype.names),
		fmt=['%s','%s','%d','%s','%s','%.4f','%.4f','%s'])

	print ''
	print 'parsed output saved to %s'%(ofname)
