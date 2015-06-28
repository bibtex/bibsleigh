#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import Fancy, AST, os.path, sys

ienputdir = '../json'
sleigh = AST.Sleigh(ienputdir)
C = Fancy.colours()
verbose = False

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
	# "url" from DBLP are useless
	if 'url' in o.json.keys() and o.json['url'].startswith('db/conf/'):
		del o.json['url']
	if 'ee' in o.json.keys() and 'doi' not in o.json.keys():
		if isinstance(o.json['ee'], list):
			if verbose:
				print(C.red('Manylink:'), o.json['ee'])
		elif o.json['ee'].startswith('http://dx.doi.org/'):
			o.json['doi'] = o.json['ee'][18:]
		elif o.json['ee'].startswith('http://doi.acm.org/'):
			o.json['doi'] = o.json['ee'][19:]
		elif o.json['ee'].startswith('http://doi.ieeecomputersociety.org/'):
			o.json['doi'] = o.json['ee'][35:]
		elif o.json['ee'].startswith('http://dl.acm.org/citation.cfm?id='):
			o.json['acmid'] = o.json['ee'][34:]
		elif o.json['ee'].startswith('http://portal.acm.org/citation.cfm?id='):
			o.json['acmid'] = o.json['ee'][38:]
		elif verbose:
			print(C.yellow('Opportunity:'), o.json['ee'])
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
