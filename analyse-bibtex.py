#!/c/Users/vadim/AppData/Local/Programs/Python/Python35/python
# -*- coding: utf-8 -*-
#
# a module for checking for compatibility of LRJs with the bibtex standard

import sys, os.path, glob
from fancy.ANSI import C
from lib.AST import Sleigh
from lib.JSON import parseJSON
# , jsonify, json2lines
# from lib.NLP import strictstrip
from fancy.BibTeX import *

ienputdir = '../json'
n2f_name = '_name2file.json'
name2file = parseJSON(n2f_name) if os.path.exists(n2f_name) else {}
sleigh = Sleigh(ienputdir + '/corpus', name2file)
verbose = False

def checkon(fn, o):
	if not os.path.exists(fn) or os.path.isdir(fn):
		fn = fn + '.json'
	# plines = sorted(json2lines(o.getJSON().split('\n')))
	if 'type' not in o.json.keys():
		return 1, 'no type specified'
	if o.get('type') not in bibtex:
		return 1, 'unknown BibTeX type “{}”'.format(o.get('type'))
	seen = set()
	extra = []
	required, optional = bibtex[o.get('type')]
	for key in o.json:
		if key.endswith('short'):
			# we operate under the assumption that if a short version is included, so is the longer one
			key = key[:-5]
		if key in required:
			seen.add(key)
		elif key in optional:
			pass
		elif key in sleighkeys:
			pass
		elif key in alwaysok:
			pass
		else:
			extra.append(key)
	if seen != required:
		return 1, 'lacking required '+ ', '.join(required - seen)
	if extra:
		return 2, 'not recognised '+ ', '.join(extra)
	return 0, 'ok'

def checkreport(fn, o):
	statuses = (C.blue('PASS'), C.red('FAIL'), C.yellow('WARN'))
	r, msg = checkon(fn, o)
	# non-verbose mode by default
	if verbose or r != 0:
		print('[ {} ] {}: {}'.format(statuses[r], fn, msg))
	return r

if __name__ == "__main__":
	verbose = sys.argv[-1] == '-v'
	peoplez = glob.glob(ienputdir + '/people/*.json')
	print('{}: {} venues, {} papers by {} people\n{}'.format(\
		C.purple('BibSLEIGH'),
		C.red(len(sleigh.venues)),
		C.red(sleigh.numOfPapers()),
		C.red(len(peoplez)),
		C.purple('='*42)))
	cx = {0: 0, 1: 0, 2: 0}
	# first, conferences and papers
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
