#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for possibly limited bulk change of values in the repo

import sys, os.path
from fancy.ANSI import C
from lib.AST import Sleigh
from lib.NLP import strictstrip

ienputdir = '../json'
n2f_name = '_name2file.json'
name2file = parseJSON(n2f_name) if os.path.exists(n2f_name) else {}
sleigh = Sleigh(ienputdir + '/corpus', name2file)
verbose = False
d2r = k2r = v2i = v2o = ''

def checkon(fn, o):
	if not os.path.exists(fn) or os.path.isdir(fn):
		fn = fn + '.json'
	if d2r and (not o.filename.startswith(d2r) or o.filename == d2r):
		return 0
	# f = open(fn, 'r')
	# lines = f.readlines()[1:-1]
	# f.close()
	# flines = [strictstrip(s) for s in lines]
	plines = sorted([strictstrip(s) for s in o.getJSON().split('\n')[1:-1]])
	if k2r in o.json.keys():
		if o.json[k2r] == v2i:
			o.json[k2r] = v2o
		else:
			return 0
	else:
		if not v2i:
			o.json[k2r] = v2o
		else:
			return 1
	nlines = sorted([strictstrip(s) for s in o.getJSON().split('\n')[1:-1]])
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
	if len(sys.argv) < 4:
		print(C.purple('BibSLEIGH'), 'usage:')
		print('\t', sys.argv[0], '<key>', '<inputValue>', '<outputValue>', '[<limit>]', '[-v]')
		sys.exit(1)
	verbose = sys.argv[-1] == '-v'
	k2r = sys.argv[1]
	v2i = sys.argv[2]
	v2o = sys.argv[3]
	if len(sys.argv) > 4:
		d2r = sys.argv[4]
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
