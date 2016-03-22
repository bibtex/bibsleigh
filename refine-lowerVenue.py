#!/c/Users/vadim/AppData/Local/Programs/Python/Python35/python
# -*- coding: utf-8 -*-
#
# a module for lowering the values of a venue, publisher, series/volume, etc
# from a conference to all its papers

import sys, os.path
from fancy.ANSI import C
from lib.AST import Sleigh

ienputdir = '../json'
n2f_name = '_name2file.json'
# name2file = parseJSON(n2f_name) if os.path.exists(n2f_name) else {}
sleigh = Sleigh(ienputdir + '/corpus', {})
verbose = False

def checkon(fn, o):
	if not os.path.exists(fn) or os.path.isdir(fn):
		fn = fn + '.json'
	changed = False
	lacking = []
	for key in ('venue', 'series', 'volume', 'publisher', 'journal', 'number'):
		if key not in o.json.keys():
			lacking.append(key)
			if key in o.up().json.keys():
				o.json[key] = o.up().json[key]
				changed = True
	if not lacking:
		return 0
	# tricky to say what is truly lacking
	if not changed:
		return 1 if 'venue' in lacking else 0
	f = open(fn, 'w', encoding='utf-8')
	f.write(o.getJSON())
	f.close()
	return 2

def checkreport(fn, o):
	statuses = (C.blue('PASS'), C.red('FAIL'), C.yellow('FIXD'))
	r = checkon(fn, o)
	# non-verbose mode by default
	if verbose or r != 0:
		print('[ {} ] {}'.format(statuses[r], fn))
	return r

if __name__ == "__main__":
	verbose = sys.argv[-1] == '-v'
	print('{}: {} venues, {} papers\n{}'.format(\
		C.purple('BibSLEIGH'),
		C.red(len(sleigh.venues)),
		C.red(sleigh.numOfPapers()),
		C.purple('='*42)))
	cx = {0: 0, 1: 0, 2: 0}
	for v in sleigh.venues:
		for c in v.getConfs():
			cx[checkreport(c.filename, c)] += 1
			for p in c.papers:
				cx[checkreport(p.filename, p)] += 1
	print('{} files checked, {} ok, {} fixed, {} failed'.format(\
		C.bold(cx[0] + cx[1] + cx[2]),
		C.blue(cx[0]),
		C.yellow(cx[2]),
		C.red(cx[1])))
