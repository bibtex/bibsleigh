#!/c/Users/vadim/AppData/Local/Programs/Python/Python35/python
# -*- coding: utf-8 -*-
#
# a module for retagging LRJs in the adjacent repository

import sys, os.path, re, glob
from fancy.ANSI import C
from lib.AST import Sleigh
from lib.JSON import parseJSON
from lib.LP import listify, uniq
from lib.NLP import strictstrip, baretext, superbaretext

ienputdir = '../json'
n2f_name = '_name2file.json'
name2file = parseJSON(n2f_name) if os.path.exists(n2f_name) else {}
sleigh = Sleigh(ienputdir + '/corpus', name2file)
verbose = False
tags = []
relieved = {}

matchModes = {\
'matchsensitive': lambda s, mcs, mes, mew, mis, miw: mcs.find(s) > -1,
'matchword':      lambda s, mcs, mes, mew, mis, miw: s in miw,
'matchwordexact': lambda s, mcs, mes, mew, mis, miw: s in mew,
'matchsub':       lambda s, mcs, mes, mew, mis, miw: mis.find(s) > -1,
'matchsubexact':  lambda s, mcs, mes, mew, mis, miw: mes.find(s) > -1,
'matchstart':     lambda s, mcs, mes, mew, mis, miw: mes.startswith(s),
'matchend':       lambda s, mcs, mes, mew, mis, miw: mes.endswith(s),
'matchre':        lambda s, mcs, mes, mew, mis, miw: re.match('^'+s+'$', mes)\
}

def checkon(fn, o):
	if os.path.isdir(fn):
		fn = fn + '.json'
	f = open(fn, 'r', encoding='utf-8')
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
			print(C.red('ERROR:'), 'no name for tag from file', t['FILE'])
			continue
		if all([not k.startswith('match') for k in t.keys()]):
			print(C.red('ERROR:'), 'no match rules for tag', t['name'])
			continue
		for k in t.keys():
			if k == 'matchentry':
				if o.getKey() in t[k]:
					ts += [t['name']]
			elif k.startswith('match'):
				ts += [t['name'] for s in listify(t[k]) if matchModes[k](s, mcs, mes, mew, mis, miw)]
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
		f = open(fn, 'w', encoding='utf-8')
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
	for rt in relieved.keys():
		print('[ {} ] {} relieved {} markings'.format(C.purple('√'), rt, relieved[rt]))
	print('{} files checked, {} ok, {} fixed, {} failed'.format(\
		C.bold(cx[0] + cx[1] + cx[2]),
		C.blue(cx[0]),
		C.yellow(cx[2]),
		C.red(cx[1])))
