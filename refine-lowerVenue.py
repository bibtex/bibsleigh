#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for lowering the value for venue from a conference to all its papers

import sys, os.path
from fancy.ANSI import C
from lib.AST import Sleigh
# from lib.NLP import strictstrip
# from lib.JSON import jsonify

ienputdir = '../json'
sleigh = Sleigh(ienputdir + '/corpus')
verbose = False

def checkon(fn, o):
	if not os.path.exists(fn) or os.path.isdir(fn):
		fn = fn + '.json'
	if 'venue' not in o.json.keys():
		if 'venue' in o.up().json.keys():
			o.json['venue'] = o.up().json['venue']
			if 'FILE' in o.json.keys():
				del o.json['FILE']
			f = open(fn, 'w')
			f.write(o.getJSON())
			f.close()
			return 2
			# TODO push series/volume and publisher to the papers as well
		else:
			return 1
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
