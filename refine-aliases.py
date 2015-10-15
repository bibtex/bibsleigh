#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for enforcing aliases

import sys, os.path, json
from fancy.ANSI import C
from fancy.Latin import nodiaLatin, simpleLatin
from lib.AST import Sleigh
from lib.JSON import parseJSON
from lib.LP import listify
from lib.NLP import strictstrip

ienputdir = '../json'
n2f_name = '_name2file.json'
name2file = parseJSON(n2f_name) if os.path.exists(n2f_name) else {}
sleigh = Sleigh(ienputdir + '/corpus', name2file)
verbose = False
renameto = {}

def checkon(fn, o):
	if not os.path.exists(fn) or os.path.isdir(fn):
		fn = fn + '.json'
	plines = sorted([strictstrip(s) for s in o.getJSON().split('\n')[1:-1]])
	for ae in ('author', 'editor'):
		if ae in o.json.keys():
			if isinstance(o.json[ae], str):
				if o.json[ae] in renameto.keys():
					o.json[ae] = renameto[o.json[ae]]
			else:
				for i, x in enumerate(o.json[ae]):
					if x in renameto.keys():
						o.json[ae][i] = renameto[x]
	nlines = sorted([strictstrip(s) for s in o.getJSON().split('\n')[1:-1]])
	if plines != nlines:
		ff = open(fn, 'w')
		ff.write(o.getJSON())
		ff.close()
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
	verbose = sys.argv[-1] == '-v'
	print('{}: {} venues, {} papers\n{}'.format(\
		C.purple('BibSLEIGH'),
		C.red(len(sleigh.venues)),
		C.red(sleigh.numOfPapers()),
		C.purple('='*42)))
	aka = parseJSON(ienputdir + '/aliases.json')
	CX = sum([len(aka[a]) for a in aka])
	# self-adaptation heuristic:
	#  if a manual rule does the same as the other heuristic, it’s dumb
	for a in sorted(aka.keys()):
		if len(aka[a]) == 1 and aka[a][0] in (nodiaLatin(a), simpleLatin(a)):
			print('[ {} ]'.format(C.blue('DUMB')), a, 'aliasing was unnecessary manual work')
		elif len(aka[a]) == 2 and (aka[a] == [nodiaLatin(a), simpleLatin(a)] \
							    or aka[a] == [simpleLatin(a), nodiaLatin(a)]):
			print('[ {} ]'.format(C.blue('DUMB')), a, 'aliasing was a lot of unnecessary manual work')
		elif nodiaLatin(a) in aka[a] or simpleLatin(a) in aka[a]:
			print('[ {} ]'.format(C.blue('DUMB')), a, 'aliasing contains some unnecessary manual work')
	# auto-aliasing heuristic:
	#  for each author with diacritics, its non-diacritic twin is considered harmful
	people = set()
	for v in sleigh.venues:
		for c in v.getConfs():
			if 'editor' in c.json:
				people.update(listify(c.json['editor']))
			for p in c.papers:
				if 'author' in p.json:
					people.update(listify(p.json['author']))
	for a in people:
		for na in (nodiaLatin(a), simpleLatin(a)):
			if na != a:
				aka.setdefault(a, [])
				aka[a].append(na)
	# invert aliasing
	for akey in aka:
		if akey in ('ZZZZZZZZZZ', 'FILE'):
			continue
		for aval in aka[akey]:
			renameto[aval] = akey
	f = open('_renameto.json', 'w', encoding='utf8')
	f.write(json.dumps(renameto, sort_keys=True, separators=(',\n\t', ': '), ensure_ascii=False))
	f.close()
	cx = {0: 0, 1: 0, 2: 0}
	for v in sleigh.venues:
		for c in v.getConfs():
			cx[checkreport(c.filename, c)] += 1
			for p in c.papers:
				cx[checkreport(p.filename, p)] += 1
	print('{} aliasing rules, {} of them manual.'.format(len(renameto), CX))
	print('{} files checked, {} ok, {} fixed, {} failed'.format(\
		C.bold(cx[0] + cx[1] + cx[2]),
		C.blue(cx[0]),
		C.yellow(cx[2]),
		C.red(cx[1])))
