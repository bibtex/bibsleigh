#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for retagging LRJs in the adjacent repository

import sys, os, re
sys.path.append(os.getcwd()+'/../engine')
import Fancy, AST, os.path, glob
from JSON import parseJSON
from LP import listify, uniq
from NLP import strictstrip, baretext, superbaretext

ienputdir = '../json'
sleigh = AST.Sleigh(ienputdir + '/corpus')
C = Fancy.colours()
verbose = False
tags = []
relieved = {}

def hcre(s):
	if s.find(': ') < 0:
		return False
	xs = s.strip().split(': ')
	return len(xs) == 2 and xs[0].isalpha() and xs[1] != ''

def checkon(fn, o):
	if os.path.isdir(fn):
		fn = fn + '.json'
	f = open(fn, 'r')
	lines = f.readlines()[1:-1]
	f.close()
	flines = [strictstrip(s) for s in lines]
	plines = sorted([strictstrip(s) for s in o.getJSON().split('\n')[1:-1]])
	ts = []
	# precise case-sensitive match
	mcs = o.get('title')
	# precise match for substrings
	mes = baretext(mcs)
	# precise match for words
	mew = mes.split(' ')
	# imprecise match for substrings
	mis = superbaretext(mes)
	# imprecise match for words
	miw = mis.split(' ')
	# now match!
	for t in tags:
		# print('Check',t,'vs',mes)
		if 'name' not in t.keys():
			print(C.red('ERROR:'), 'no name for tag from tile', t['FILE'])
			continue
		if 'matchword' not in t.keys() and 'matchsub' not in t.keys() and \
		'matchwordexact' not in t.keys() and 'matchsubexact' not in t.keys() and\
		'matchre' not in t.keys() and\
		'matchend' not in t.keys() and 'matchsensitive' not in t.keys():
			print(C.red('ERROR:'), 'no match rules for tag', t['name'])
			continue
		if 'matchsensitive' in t.keys():
			ts.extend([t['name'] for s in listify(t['matchsensitive']) if mcs.find(s) > -1])
		if 'matchword' in t.keys():
			ts.extend([t['name'] for w in listify(t['matchword']) if w in miw])
		if 'matchwordexact' in t.keys():
			ts.extend([t['name'] for w in listify(t['matchwordexact']) if w in mew])
		if 'matchsub' in t.keys():
			ts.extend([t['name'] for s in listify(t['matchsub']) if mis.find(s) > -1])
		if 'matchsubexact' in t.keys():
			ts.extend([t['name'] for s in listify(t['matchsubexact']) if mes.find(s) > -1])
		if 'matchend' in t.keys():
			ts.extend([t['name'] for s in listify(t['matchend']) if mes.endswith(s)])
		if 'matchre' in t.keys():
			# r = re.compile('^' + t['matchre'] + '$')
			# ts.extend([t['name'] for r in listify(t['matchre']) if re.match('^' + r + '$', mes)])
			ts.extend([t['name'] for r in listify(t['matchre']) if hcre(mes)])
	# second pass: check reliefs
	for t in tags:
		if 'relieves' in t.keys():
			for r in listify(t['relieves']):
				if t['name'] in ts and r in ts:
					ts.remove(r)
					if t['name'] not in relieved.keys():
						relieved[t['name']] = 0
					relieved[t['name']] += 1
	if ts:
		if not o.tags:
			o.tags = []
		for t in ts:
			if t not in o.tags:
				o.tags.append(t)
		# uncomment the following one line to overwrite all tags
		o.tags = uniq(ts)
		# let’s keep tags clean and sorted
		o.tags = sorted(o.tags)
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
	tags = [parseJSON(tfn) for tfn in glob.glob(ienputdir + '/tags/*.json')]
	print('{}: {} tags, {} venues, {} papers\n{}'.format(\
		C.purple('BibSLEIGH'),
		C.red(len(tags)),
		C.red(len(sleigh.venues)),
		C.red(sleigh.numOfPapers()),
		C.purple('='*42)))
	cx = {0: 0, 1: 0, 2: 0}
	for v in sleigh.venues:
		for c in v.getConfs():
			# NB: We don’t tag conferences. Should we?
			# cx[checkreport(c.filename, c)] += 1
			for p in c.papers:
				cx[checkreport(p.filename, p)] += 1
	for t in relieved.keys():
		print('[ {} ] {} relieved {} markings'.format(C.purple('√'), t, relieved[t]))
	print('{} files checked, {} ok, {} fixed, {} failed'.format(\
		C.bold(cx[0] + cx[1] + cx[2]),
		C.blue(cx[0]),
		C.yellow(cx[2]),
		C.red(cx[1])))
