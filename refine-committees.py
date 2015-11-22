#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for enriching conference definitions with chairs/committees

import sys, os.path
from fancy.ANSI import C
from lib.AST import Sleigh
from lib.JSON import parseJSON
from lib.NLP import nrs, strictstrip

ienputdir = '../json'
rt_name = '_renameto.json'
renameto = parseJSON(rt_name) if os.path.exists(rt_name) else {}
# FIXME
mr = parseJSON('_established.json')
for m in mr.keys():
	if m not in renameto.keys():
		renameto[m] = mr[m]
sleigh = Sleigh(ienputdir + '/corpus', {})
verbose = False
lookat = []
roles = {}

def checkon(fn, o):
	if not os.path.exists(fn) or os.path.isdir(fn):
		fn = fn + '.json'
	if o.get('type') not in ('proceedings', 'book'):
		# we don't go per paper
		return 0
	if o.getKey() not in roles.keys():
		# you know nothing, scraped CSV
		return 0
	plines = sorted([strictstrip(s) for s in o.getJSON().split('\n')[1:-1]])
	# if 'roles' not in o.json.keys():
	if True:
		# no prior knowledge of roles => we know everything
		o.json['roles'] = sorted(roles[o.getKey()], key=lambda x: x[1])
	else:
		# prior knowledge of roles => treat per case
		o.json['roles'] = sorted(o.json['roles'] + [r for r in roles[o.getKey()] if r not in o.json['roles']], key=lambda x: x[1])
	nlines = sorted([strictstrip(s) for s in o.getJSON().split('\n')[1:-1]], key=lambda x: x[1])
	# The next case should not happen, but could if we have trivial lists
	# if flines != plines:
	# 	return 1
	if plines != nlines:
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
	# read the CSV
	f = open('scrap-committees/scraped-by-grammarware.csv', 'r')
	# CBSE;2001;Heinz;Schmidt;;Organising Committee
	for line in f.readlines():
		vs = line.strip().split(';')
		if len(vs) == 0:
			continue
		v = vs[0] + '-' + vs[1]
		n = vs[2] + ' ' + vs[3]
		# normalise!
		if n in renameto.keys():
			print('[', C.yellow('ALIA'), ']', 'Treating', n, 'as', renameto[n])
			n = renameto[n]
		# sex is ignored, mostly absent anyway
		r = vs[5]
		if v not in roles.keys():
			roles[v] = []
		# NB: the next line uses lists for the sake of JSON compatibility
		roles[v].append([n,r])
	f.close()
	print('Metadata on {} editions loaded with {} role assignments'.format(C.red(len(roles)), C.red(sum([len(roles[k]) for k in roles.keys()]))))
	# now add
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
	for f in lookat:
		print('\t'+f)
