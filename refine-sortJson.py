#!/c/Users/vadim/AppData/Local/Programs/Python/Python35/python
# -*- coding: utf-8 -*-
#
# a module for sorting the key-value pairs within each LRJ

import sys, os.path, glob
from fancy.ANSI import C
from lib.AST import Sleigh
from lib.JSON import parseJSON, jsonify, json2lines
from lib.NLP import strictstrip

ienputdir = '../json'
n2f_name = '_name2file.json'
name2file = parseJSON(n2f_name) if os.path.exists(n2f_name) else {}
sleigh = Sleigh(ienputdir + '/corpus', name2file)
verbose = False

def guessYear(p):
	cys = [int(w) for w in p.split('-') if len(w) == 4 and w.isdigit()]
	if len(cys) == 1:
		return cys[0]
	else:
		j = sleigh.seekByKey(p)
		if j and 'year' in j.json.keys():
			return j.get('year')
		elif 'year' in dir(j):
			return j.year
		else:
			print('[ {} ] {}'.format(C.red('YEAR'), p))
			return 0

def checkon(fn, o):
	if not os.path.exists(fn) or os.path.isdir(fn):
		fn = fn + '.json'
	f = open(fn, 'r', encoding='utf-8')
	lines = f.readlines()[1:-1]
	f.close()
	flines = json2lines(lines)
	plines = sorted(json2lines(o.getJSON().split('\n')))
	if flines != plines:
		f1 = [line for line in flines if line not in plines]
		f2 = [line for line in plines if line not in flines]
		if f1 or f2:
			if verbose:
				print('∆:', f1, 'vs', f2)
			print('F-lines:', '\n'.join(flines))
			print('P-lines:', '\n'.join(plines))
			return 1
		else:
			f = open(fn, 'w', encoding='utf-8')
			f.write(o.getJSON())
			f.close()
			return 2
	else:
		return 0

def checkreport(fn, o):
	statuses = (C.blue('PASS'), C.red('FAIL'), C.yellow('FIXD'))
	if isinstance(o, int):
		r = o
	else:
		r = checkon(fn, o)
	# non-verbose mode by default
	if verbose or r != 0:
		print('[ {} ] {}'.format(statuses[r], fn))
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
		for b in v.getBrands():
			cx[checkreport(b.filename, b)] += 1
		for c in v.getConfs():
			cx[checkreport(c.filename, c)] += 1
			for p in c.papers:
				cx[checkreport(p.filename, p)] += 1
	# then, people
	for fn in peoplez:
		per = parseJSON(fn)
		if 'authored' not in per.keys() and 'roles' not in per.keys():
			cx[checkreport(fn, 0)] += 1
			continue
		changed = False
		if 'authored' in per.keys():
			ps = {}
			for p in per['authored']:
				y = guessYear(p)
				if y not in ps.keys():
					ps[y] = []
				ps[y].append(p)
			rps = []
			for y in sorted(ps.keys(), reverse=True):
				rps += sorted(ps[y])
			if rps != per['authored']:
				changed = True
				per['authored'] = rps
		if 'roles' in per.keys():
			ps = {}
			for pair in per['roles']:
				y = guessYear(pair[0])
				if y not in ps.keys():
					ps[y] = []
				ps[y].append(pair)
			rps = []
			for y in sorted(ps.keys(), reverse=True):
				# print('PS[Y] =', ps[y])
				rps += sorted(ps[y])
			if rps != per['roles']:
				changed = True
				per['roles'] = rps
		# Decide whether to update
		if changed:
			cx[checkreport(fn, 2)] += 1
			f = open(fn, 'w', encoding='utf-8')
			del per['FILE']
			f.write(jsonify(per))
			f.close()
		else:
			cx[checkreport(fn, 0)] += 1
	print('{} files checked, {} ok, {} fixed, {} failed'.format(\
		C.bold(cx[0] + cx[1] + cx[2]),
		C.blue(cx[0]),
		C.yellow(cx[2]),
		C.red(cx[1])))
