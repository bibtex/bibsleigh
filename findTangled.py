#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import Fancy, AST, sys

ienputdir = '../json'
sleigh = AST.Sleigh(ienputdir)
C = Fancy.colours()
verbose = False

def report(fn, r):
	statuses = (C.blue('PASS'), C.red('FAIL'), C.yellow('UNEX'))
	special = ('', '- no crossref found!', '- illegal crossref')
	# non-verbose mode by default
	if verbose or r != 0:
		print('[ {} ] {} {}'.format(statuses[r], fn, special[r]))
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
			if 'dblpkey' not in c.json.keys():
				cx[report(c.filename, 1)] += 1
				continue
			for p in c.papers:
				if 'crossref' not in p.json.keys():
					cx[report(p.filename, 1)] += 1
				elif p.json['crossref'] == c.json['dblpkey']:
					cx[report(p.filename, 0)] += 1
				else:
					cx[report(p.filename, 2)] += 1
	print('{} files checked, {} ok, {} fixed, {} failed'.format(\
		C.bold(cx[0] + cx[1] + cx[2]),
		C.blue(cx[0]),
		C.yellow(cx[2]),
		C.red(cx[1])))
