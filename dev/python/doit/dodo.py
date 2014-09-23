"""
My first doit 'makefile'
"""

from doit.tools import run_once

fbgn='iamthebeginning.txt'
def task_beginning():
	return {
			'actions': ['touch {}'.format(fbgn)],
			'targets': [fbgn],
			'uptodate': [run_once]
			}

def task_hello():
	"""hello"""

	def python_hello(targets):
		with open(targets[0], "a") as output:
			output.write("Python says Hello World!!!\n")

	return {
			'actions': [python_hello],
			'targets': ["hello.txt"],
			}

def task_hello2():
	"""second hello"""

	msg = 3*'hi!'
	return {
			'actions': ['echo {} >> %(targets)s'.format(msg) ],
			'targets': ['hello2.txt'],
			'file_dep': [fbgn]
			}

def task_hellomon():
	"""monitors hello"""

	def print_linecount(fname):
		with open(fname, 'r') as f:
			lines = f.readlines()
		print '{} has {:d} lines.'.format(
				fname, len(lines))

	return {
			'actions': [(print_linecount,['hello2.txt'])],
			'verbosity': 2,
			'file_dep': ['hello2.txt']
			}

def task_python_version():
	return {
		'actions': [['python', '--version']],
		'file_dep': ['dodo.py']
	}
