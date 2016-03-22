#!/c/Users/vadim/AppData/Local/Programs/Python/Python35/python
# -*- coding: utf-8 -*-
#
# a module for lifting information common within papers from the same venue, to the venue itself

import sys, os.path
from fancy.ANSI import C
from lib.AST import Sleigh
from lib.NLP import heurichoose

ienputdir = '../json'
n2f_name = '_name2file.json'
name2file = parseJSON(n2f_name) if os.path.exists(n2f_name) else {}
sleigh = Sleigh(ienputdir + '/corpus', name2file)
verbose = False

def checkon(m, o):
	# if no common model found, we failed
	if not m:
		return 1
	if 'type' in m.keys() and m['type'] in ('inproceedings', 'article'):
		m['type'] = 'proceedings'
	if 'crossref' in m.keys():
		del m['crossref']
	if 'booktitle' in m.keys():
		m['title'] = m['booktitle']
		del m['booktitle']
	if 'booktitleshort' in m.keys():
		# TODO: ???
		del m['booktitleshort']
	r = 0
	n = {}
	for k in m.keys():
		if o.get(k) == m[k]:
			if verbose:
				print(C.blue('Confirmed:  '), k, 'as', m[k])
		else:
			if verbose:
				print(C.red('Conflicted: '), k, 'as', m[k], 'vs', o.get(k))
			v = heurichoose(k, m[k], o.json[k]) if k in o.json.keys() else m[k]
			if verbose:
				print(C.yellow('Settled for:'), v)
			n[k] = v
			r = 2
	if r == 0:
		return r
	if r == 2 and not n:
		# nothing to fix?!
		return 0
	if not os.path.exists(o.filename):
		return 0
	if os.path.isdir(o.filename):
		fn = o.filename + '.json'
	else:
		fn = o.filename
	f = open(fn, 'r', encoding='utf-8')
	lines = f.read()
	f.close()
	if lines != o.getJSON():
		# strange, should be equal (run all normalisers first!)
		return 1
	for k in n.keys():
		o.json[k] = n[k]
	f = open(fn, 'w', encoding='utf-8')
	f.write(o.getJSON())
	f.close()
	return 2

def updatemodel(m, o):
	if 'GO' in m:
		m.clear()
		return o.json.copy()
	else:
		return {k:m[k] for k in m.keys() if m[k] == o.get(k)}

def checkreport(m, o):
	statuses = (C.blue('PASS'), C.red('FAIL'), C.yellow('FIXD'))
	r = checkon(m, o)
	# non-verbose mode by default
	if verbose or r != 0:
		print('[ {} ] {}'.format(statuses[r], o.filename))
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
	for vv in sleigh.venues:
		for c in vv.getConfs():
			model = {'GO': 1}
			for p in c.papers:
				model = updatemodel(model, p)
			cx[checkreport(model, c)] += 1
	print('{} files checked, {} ok, {} fixed, {} failed'.format(\
		C.bold(cx[0] + cx[1] + cx[2]),
		C.blue(cx[0]),
		C.yellow(cx[2]),
		C.red(cx[1])))
