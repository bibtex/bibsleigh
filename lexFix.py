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
	flines = f.readlines()[1:-1]
	f.close()
	sflines = [strictstrip(s) for s in flines]
	sjlines = sorted([strictstrip(s) for s in o.getJSON().split('\n')[1:-1]])
	jlines = ['\t{},\n'.format(s) for s in sjlines]
	jlines[-1] = jlines[-1][:-2] + '\n' # remove the last comma
	if sflines != sjlines:
		return 1
	elif jlines != flines:
		# f1 = [s for s in jlines if s not in flines]
		# f2 = [s for s in flines if s not in jlines]
		# print('∆:', f1, '\nvs', f2)
		f = open(fn, 'w')
		f.write('{\n')
		for line in jlines:
			f.write(line)
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
		C.red(cx[1])))
