#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for assigning proper names to papers, venues and journals

import sys, os.path
from fancy.ANSI import C
from lib.AST import Sleigh
from lib.NLP import strictstrip
from fancy.KnownNames import badvariants, contractions

ienputdir = '../json'
sleigh = Sleigh(ienputdir + '/corpus')
verbose = False
wheretolook = ('journal', 'series', 'booktitle', 'publisher')

def checkon(fn, o):
	if not os.path.exists(fn) or os.path.isdir(fn):
		fn = fn + '.json'
	f = open(fn, 'r')
	lines = f.readlines()[1:-1]
	f.close()
	flines = [strictstrip(s) for s in lines]
	plines = sorted([strictstrip(s) for s in o.getJSON().split('\n')[1:-1]])
	# bad variants
	for bad, good in badvariants:
		for key in wheretolook:
			if o.get(key) == bad:
				o.json[key] = good
	# contractions
	for short, longer in contractions:
		for key in wheretolook:
			if o.get(key) == short:
				o.json[key] = longer
			if o.get(key) == longer:
				o.json[key+'short'] = short
	# a heuristic contraction for conference names
	if o.get('type') == 'inproceedings' \
	and 'booktitleshort' not in o.json.keys() \
	and 'booktitle' in o.up().json.keys() \
	and len(o.get('booktitle')) > len(o.up().get('booktitle')):
		o.json['booktitleshort'] = o.up().get('booktitle')
	# Springer name change
	if o.get('publisher').find('Springer') > -1 and 'year' in o.json.keys():
		if int(o.get('year')) < 2002:
			o.json['publisher'] = 'Springer-Verlag'
			o.json['publishershort'] = 'Springer'
		else:
			o.json['publisher'] = 'Springer International Publishing'
			o.json['publishershort'] = 'Springer'
	# superfluosness
	for key in wheretolook:
		if key in o.json.keys() and key+'short' in o.json.keys() \
		and o.get(key) == o.get(key+'short'):
			del o.json[key+'short']
	nlines = sorted([strictstrip(s) for s in o.getJSON().split('\n')[1:-1]])
	if flines != plines:
		return 1
	elif plines != nlines:
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
