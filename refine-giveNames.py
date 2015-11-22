#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for assigning proper names to papers, venues and journals

import sys, os.path
from fancy.ANSI import C
from fancy.KnownNames import unfoldName, short2long
from lib.AST import Sleigh
from lib.JSON import parseJSON, json2lines

ienputdir = '../json'
n2f_name = '_name2file.json'
name2file = parseJSON(n2f_name) if os.path.exists(n2f_name) else {}
sleigh = Sleigh(ienputdir + '/corpus', name2file)
verbose = False
wheretolook = ('journal', 'series', 'booktitle', 'publisher')

def checkon(fn, o):
	if not os.path.exists(fn) or os.path.isdir(fn):
		fn = fn + '.json'
	f = open(fn, 'r')
	lines = f.readlines()[1:-1]
	f.close()
	flines = json2lines(lines)
	plines = sorted(json2lines(o.getJSON().split('\n')))
	# bad variants
	for bad in unfoldName:
		for key in wheretolook:
			if o.get(key) == bad:
				o.json[key] = unfoldName[bad]
	# contractions
	for short in short2long:
		for key in wheretolook:
			if o.get(key) == short:
				o.json[key] = short2long[short]
			if o.get(key) == short2long[short]:
				o.json[key+'short'] = short
	# a heuristic contraction for conference names
	if o.get('type') == 'inproceedings' \
	and 'booktitleshort' not in o.json.keys() \
	and 'booktitle' in o.up().json.keys() \
	and len(o.get('booktitle')) > len(o.up().get('booktitle')):
		o.json['booktitleshort'] = o.up().get('booktitle')
	# a heuristic expansion of conference names
	# if o.get('type') == 'proceedings' \
	# and 'booktitleshort' not in o.json.keys() \
	# and 'booktitle' in o.up().json.keys() \
	# and len(o.get('booktitle')) > len(o.up().get('booktitle')):
	# 	o.json['booktitleshort'] = o.up().get('booktitle')
	# remove faulty series: journal wins
	if 'series' in o.json and 'journal' in o.json and o.get('series') == o.get('journal'):
		del o.json['series']
	# *short legacy while no longer version present
	for key in [k for k in o.json.keys() if k.endswith('short') and k[:-5] not in o.json.keys()]:
		del o.json[key]
	# Springer name change
	if o.get('publisher').find('Springer') > -1 and 'year' in o.json.keys():
		if int(o.get('year')) < 2002:
			o.json['publisher'] = 'Springer-Verlag'
			o.json['publishershort'] = 'Springer'
		else:
			o.json['publisher'] = 'Springer International Publishing'
			o.json['publishershort'] = 'Springer'
	for key in wheretolook:
		if key not in o.json:
			continue
		val = o.get(key)
		# ends with a dot
		if val.endswith('.'):
			o.json[key] = o.json[key][:-1]
			continue
		# suspiciousness
		if val.find('.') > -1:
			problem = True
			for ok in ('. Volume', 'CEUR-WS.org', 'icml.cc', 'JMLR.org', 'Vol. ', '. Part', \
				' Inc. ', 'WG2.8'):
				if val.find(ok) > -1:
					problem = False
					break
			if problem:
				report(C.yellow('LOOK'), key + ' of ' + o.getKey() + ' is “' + o.get(key) + '”')
		# superfluousness
		if key+'short' in o.json.keys() and val == o.get(key+'short'):
			del o.json[key+'short']
	nlines = sorted(json2lines(o.getJSON().split('\n')))
	if flines != plines:
		return 1
	elif plines != nlines:
		f = open(fn, 'w')
		f.write(o.getJSON())
		f.close()
		return 2
	else:
		return 0

def report(one, two):
	print('[ {} ] {}'.format(one, two))

def checkreport(fn, o):
	statuses = (C.blue('PASS'), C.red('FAIL'), C.yellow('FIXD'))
	r = checkon(fn, o)
	# non-verbose mode by default
	if verbose or r != 0:
		report(statuses[r], fn)
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
