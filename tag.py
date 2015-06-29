#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.getcwd()+'/../engine')
import Fancy, AST, os.path

ienputdir = '../json'
sleigh = AST.Sleigh(ienputdir)
C = Fancy.colours()
verbose = False
# TODO: support tag aliases
tagz = []

def strictstrip(s):
	s = s.strip()
	if s.endswith(','):
		s = s[:-1]
	return s

def tagpositive(what, where):
	# tags without spaces in them are more reliable
	for x in ',.:!./\“”‘’-_=':
		where = where.replace(x, ' ')
	where = where.strip().lower()
	while where.find('  ') > -1:
		where = where.replace('  ', ' ')
	if what.find(' ') < 0:
		return what in where.split(' ')
	else:
		return where.find(what) > -1

def checkon(fn, o):
	if os.path.isdir(fn):
		fn = fn + '.json'
	f = open(fn, 'r')
	lines = f.readlines()[1:-1]
	f.close()
	flines = [strictstrip(s) for s in lines]
	plines = sorted([strictstrip(s) for s in o.getJSON().split('\n')[1:-1]])
	ts = []
	for t in tagz:
		if tagpositive(t, o.get('title')):
			ts.append(t)
	if ts:
		if not o.tags:
			o.tags = []
		for t in ts:
			if t not in o.tags:
				o.tags.append(t)
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
	f = open('tags.txt', 'r')
	for line in f.readlines():
		line = line.strip()
		if line:
			tagz.append(line)
	f.close()
	print('{}: {} tags, {} venues, {} papers\n{}'.format(\
		C.purple('BibSLEIGH'),
		C.red(len(tagz)),
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
