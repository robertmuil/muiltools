##Start debug functions
##The following debug functions are utilized by this 'utils' module,
## but can also be copy and pasted into other modules.
try:
		dbg_lvl# @UndefinedVariable
		#print '%s.dbg_lvl == %d' % ('utils', dbg_lvl)
except NameError:
		dbg_lvl = 1

def dbg(lvl, msg):
		if lvl <= dbg_lvl:
				if lvl == 0:
						print '%s'%msg
				else:
						caller_name = inspect.stack()[1][3]
						print('dbg(%d|%s): %s'%(lvl, caller_name, msg))

def set_dbg_lvl(new_dbg_lvl):
		global dbg_lvl
		dbg_lvl = new_dbg_lvl
##End debug functions
