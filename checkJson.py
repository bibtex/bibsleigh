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
	flines = sorted([strictstrip(s) for s in lines])
	plines = sorted([strictstrip(s) for s in o.getJSON().split('\n')[1:-1]])
	if flines != plines:
		f1 = [line for line in flines if line not in plines]
		f2 = [line for line in plines if line not in flines]
		print('∆:', f1, '\nvs', f2)
	return flines == plines

def checkreport(fn, o):
	if checkon(fn, o):
		status = C.blue('PASS')
	else:
		status = C.red('FAIL')
	print('[ {} ] {}'.format(status, fn))
	return status

if __name__ == "__main__":
	print('{}: {} venues, {} papers\n{}'.format(\
		C.purple('BibSLEIGH'),
		C.red(len(sleigh.venues)),
		C.red(sleigh.numOfPapers()),
		C.purple('='*42)))
	ok = er = 0
	for v in sleigh.venues:
		for c in v.getConfs():
			if checkreport(c.filename, c):
				ok += 1
			else:
				er += 1
			for p in c.papers:
				if checkreport(p.filename, p):
					ok += 1
				else:
					er += 1
	print('{} files checked, {} ok, {} failed'.format(\
		C.bold(ok+er),
		C.blue(ok),
		C.red(er) ))
