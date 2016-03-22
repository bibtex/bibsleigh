#!/c/Users/vadim/AppData/Local/Programs/Python/Python35/python
# -*- coding: utf-8 -*-
#
# a module for analysing tagging per entity

import sys, os.path, glob
from fancy.ANSI import C
from lib.AST import Sleigh, last
from lib.JSON import parseJSON, json2lines

ienputdir = '../json'
n2f_name = '_name2file.json'
name2file = parseJSON(n2f_name) if os.path.exists(n2f_name) else {}
sleigh = Sleigh(ienputdir + '/corpus', name2file)
verbose = False

def checkon(fn, o):
	if not os.path.exists(fn):
		print('Path does not exist:', fn)
		return 1
	if os.path.isdir(fn):
		if os.path.exists(fn+'.json'):
			fn = fn + '.json'
		elif os.path.exists(fn+'/'+last(fn)+'.json'):
			fn = fn+'/'+last(fn)+'.json'
		else:
			print('Where to find', fn, '?')
			return 1
	plines = sorted(json2lines(o.getJSON().split('\n')))
	o.getQTags()
	flines = sorted(json2lines(o.getJSON().split('\n')))
	if flines != plines:
		if verbose:
			print('∆:', '\n'.join([line for line in flines if line not in plines]))
			print('vs', '\n'.join([line for line in plines if line not in flines]))
		f = open(fn, 'w', encoding='utf-8')
		f.write(o.getJSON())
		f.close()
		return 2
	else:
		return 0

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
		# tags per venue
		for c in v.getConfs():
			cx[checkreport(c.filename, c)] += 1
		for b in v.brands:
			cx[checkreport(b.filename, b)] += 1
		cx[checkreport(v.filename, v)] += 1
	print('{} files checked, {} ok, {} fixed, {} failed'.format(\
		C.bold(cx[0] + cx[1] + cx[2]),
		C.blue(cx[0]),
		C.yellow(cx[2]),
		C.red(cx[1])))
