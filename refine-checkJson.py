#!/c/Users/vadim/AppData/Local/Programs/Python/Python35/python
# -*- coding: utf-8 -*-
#
# a module for simply traversing all the LRJs and reading them in
# if you run this and it fails, you’re in big trouble

import sys, os.path
from lib.AST import Sleigh
from lib.NLP import strictstrip
from lib.LP import lastSlash
from fancy.ANSI import C

ienputdir = '../json'
n2f_name = '_name2file.json'
# name2file = parseJSON(n2f_name) if os.path.exists(n2f_name) else {}
sleigh = Sleigh(ienputdir + '/corpus', {})
verbose = False

def findYear(fn):
	return int(''.join([ch for ch in fn if ch.isdigit()]))

def checkon(fn, o):
	if not os.path.exists(fn) or os.path.isdir(fn):
		fn = fn + '.json'
	if not os.path.exists(fn):
		# if it still does not exist, let us create a minimal one
		f = open(fn, 'w', encoding='utf-8')
		f.write('{{\n\t"title": "{name}",\n\t"type": "proceedings",\n\t"year": {year}\n}}'.format(\
			name=lastSlash(fn)[:-5].replace('-', ' '),
			year=findYear(lastSlash(fn))\
		))
		f.close()
		print('[ {} ] {}'.format(C.yellow('MADE'), fn))
		return 2
	f = open(fn, 'r', encoding='utf-8')
	lines = f.readlines()[1:-1]
	f.close()
	for line in lines:
		if line.find('"year"') > -1 and findYear(line) > 3000:
			os.remove(fn)
			print('[ {} ] {}'.format(C.red('KILL'), fn))
			return 1
	flines = sorted([strictstrip(s) for s in lines])
	plines = sorted([strictstrip(s) for s in o.getJSON().split('\n')[1:-1]])
	if flines != plines:
		f1 = [line for line in flines if line not in plines]
		f2 = [line for line in plines if line not in flines]
		print('∆:', f1, '\nvs', f2)
	if flines == plines:
		return 0
	else:
		return 1

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
	print('{} files checked, {} ok, {} created, {} failed'.format(\
		C.bold(cx[0] + cx[1] + cx[2]),
		C.blue(cx[0]),
		C.yellow(cx[2]),
		C.red(cx[1])))
