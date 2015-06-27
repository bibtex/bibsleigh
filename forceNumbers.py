#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import Fancy, AST, os.path

ienputdir = '../json'
sleigh = AST.Sleigh(ienputdir)
C = Fancy.colours()

def strictstrip(s):
	s = s.strip()
	if s.endswith(','):
		s = s[:-1]
	return s

def checkon(fn, o):
	if os.path.isdir(fn):
		fn = fn + '.json'
	f = open(fn, 'r')
	lines = f.readlines()[1:-1]
	f.close()
	flines = [strictstrip(s) for s in lines]
	plines = sorted([strictstrip(s) for s in o.getJSON().split('\n')[1:-1]])
	for k in o.json.keys():
		if isinstance(o.json[k], str) and o.json[k].isdigit():
			o.json[k] = int(o.json[k])
	nlines = sorted([strictstrip(s) for s in o.getJSON().split('\n')[1:-1]])
	if flines != plines:
		return 1
	elif plines != nlines:
		f = open(fn, 'w')
		f.write('{\n')
		for line in nlines:
			f.write('\t'+line+'\n')
		f.write('}')
		f.close()
		return 2
	else:
		return 0

def checkreport(fn, o):
	statuses = (C.blue('PASS'), C.red('FAIL'), C.yellow('FIXD'))
	r = checkon(fn, o)
	print('[ {} ] {}'.format(statuses[r], fn))
	return r

if __name__ == "__main__":
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
		C.red(cx[1]) ))
