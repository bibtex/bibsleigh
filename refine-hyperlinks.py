#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for cleaning up links

import sys, os, os.path
from fancy.ANSI import C
from lib.AST import Sleigh
from lib.JSON import parseJSON, json2lines
from lib.LP import listify
from lib.NLP import strictstrip

ienputdir = '../json'
n2f_name = '_name2file.json'
name2file = parseJSON(n2f_name) if os.path.exists(n2f_name) else {}
sleigh = Sleigh(ienputdir + '/corpus', name2file)
verbose = False

def checkon(fn, o):
	if not os.path.exists(fn) or os.path.isdir(fn):
		fn = fn + '.json'
	f = open(fn, 'r')
	lines = f.readlines()[1:-1]
	f.close()
	flines = json2lines(lines)
	plines = sorted(json2lines(o.getJSON().split('\n')))
	# "url" from DBLP are useless
	if 'url' in o.json.keys():
		o.json['url'] = [link for link in listify(o.json['url'])\
		 				if not link.startswith('db/conf/')\
		 				and not link.startswith('db/series/')\
						and not link.startswith('db/journals/')]
		if not o.json['url']:
			del o.json['url']
		elif len(o.json['url']) == 1:
			o.json['url'] = o.json['url'][0]
	if 'ee' in o.json.keys() and 'doi' not in o.json.keys():
		if isinstance(o.json['ee'], list):
			if verbose:
				print(C.red('Manylink:'), o.json['ee'])
		for onelink in listify(o.json['ee']):
			if onelink.startswith('http://dx.doi.org/'):
				o.json['doi'] = onelink[18:]
			elif onelink.startswith('http://doi.acm.org/'):
				o.json['doi'] = onelink[19:]
			elif onelink.startswith('http://doi.ieeecomputersociety.org/'):
				o.json['doi'] = onelink[35:]
			elif onelink.startswith('http://dl.acm.org/citation.cfm?id='):
				o.json['acmid'] = onelink[34:]
			elif onelink.startswith('http://portal.acm.org/citation.cfm?id='):
				o.json['acmid'] = onelink[38:]
			elif verbose:
				print(C.yellow('Missed opportunity:'), onelink)
		# post-processing normalisation
		if 'acmid' in o.json.keys() and o.json['acmid'].isdigit():
			o.json['acmid'] = int(o.json['acmid'])
	if 'eventuri' in o.json.keys():
		o.json['eventurl'] = o.json['eventuri']
		del o.json['eventuri']
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
