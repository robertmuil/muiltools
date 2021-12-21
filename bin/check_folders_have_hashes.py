#!/usr/bin/env python
IGNORE=['.ipynb_checkpoints']

import pathlib
from pprint import pprint

p_base = pathlib.Path('.')
p_base

hashes = {}
for p_sub in p_base.iterdir():
	if p_sub.is_dir() and (p_sub.name not in IGNORE):
		hashes[p_sub.name] = []

		for yes in p_sub.glob('_dirhash*'):
			hashes[p_sub.name] += [yes.name]

pprint(hashes)

if False:
	TODO sdomething about this doesnt work
	missing_hashes={k for h,v in hashes.items() if len(hashes[v]) < 1}
	pprint(missing_hashes)
	if len(missing_hashes) > 1:
		print(f'{len(missing_hashes):d} folders missing _dirhash_* file')
		pprint(missing_hashes)
	else:
		print('all good!')
