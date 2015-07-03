#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for sorting the key-value pairs within each LRJ

import sys, os
sys.path.append(os.getcwd()+'/../engine')
import Fancy, AST, os.path
from NLP import strictstrip

ienputdir = '../json'
sleigh = AST.Sleigh(ienputdir + '/corpus')
C = Fancy.colours()
verbose = False

def checkon(fn, o):
	if os.path.isdir(fn):
		fn = fn + '.json'
	f = open(fn, 'r')
	lines = f.readlines()[1:-1]
	f.close()
	flines = [strictstrip(s) for s in lines]
	plines = sorted([strictstrip(s) for s in o.getJSON().split('\n')[1:-1]])
	if flines != plines:
		f1 = [line for line in flines if line not in plines]
		f2 = [line for line in plines if line not in flines]
		if f1 or f2:
			if verbose:
				print('∆:', f1, 'vs', f2)
			return 1
		else:
			f = open(fn, 'w')
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
	if len(sys.argv) > 1:
		verbose = sys.argv[1] == '-v'
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
