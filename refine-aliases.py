#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for enforcing aliases

import sys, os.path
from fancy.ANSI import C
from lib.AST import Sleigh
from lib.JSON import parseJSON
from lib.NLP import strictstrip

ienputdir = '../json'
sleigh = Sleigh(ienputdir + '/corpus')
verbose = False
renameto = {}

def checkon(fn, o):
	if not os.path.exists(fn) or os.path.isdir(fn):
		fn = fn + '.json'
	# f = open(fn, 'r')
	# lines = f.readlines()[1:-1]
	# f.close()
	# flines = [strictstrip(s) for s in lines]
	plines = sorted([strictstrip(s) for s in o.getJSON().split('\n')[1:-1]])
	for ae in ('author', 'editor'):
		if ae in o.json.keys():
			if isinstance(o.json[ae], str):
				if o.json[ae] in renameto.keys():
					o.json[ae] = renameto[o.json[ae]]
			else:
				for i, a in enumerate(o.json[ae]):
					if a in renameto.keys():
						o.json[ae][i] = renameto[a]
	nlines = sorted([strictstrip(s) for s in o.getJSON().split('\n')[1:-1]])
	# The next case should not happen, but could if we have trivial lists
	# if flines != plines:
	# 	return 1
	if plines != nlines:
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
	verbose = sys.argv[-1] == '-v'
	print('{}: {} venues, {} papers\n{}'.format(\
		C.purple('BibSLEIGH'),
		C.red(len(sleigh.venues)),
		C.red(sleigh.numOfPapers()),
		C.purple('='*42)))
	aka = parseJSON(ienputdir + '/aliases.json')
	# invert aliasing
	for akey in aka.keys():
		for aval in aka[akey]:
			renameto[aval] = akey
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
