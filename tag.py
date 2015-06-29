#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.getcwd()+'/../engine')
import Fancy, AST, os.path

ienputdir = '../json'
sleigh = AST.Sleigh(ienputdir)
C = Fancy.colours()
verbose = False
tagz = []
tagliases = {}
tagkillz = {}

def strictstrip(s):
	s = s.strip()
	if s.endswith(','):
		s = s[:-1]
	return s

def tagpositive(what, where):
	# tags without spaces in them are more reliable
	for x in ',.:!?;./\“”‘’–—_=@$%^&()[]\{\}§±`~<>|\'':
		# we still need # (because C# and F#) and + (do you have to ask?)
		where = where.replace(x, ' ')
	where = where.strip().lower()
	while where.find('  ') > -1:
		where = where.replace('  ', ' ')
	if what.find(' ') < 0:
		return what in where.split(' ')
	else:
		return where.find(what) > -1

def checkon(fn, o):
	if os.path.isdir(fn):
		fn = fn + '.json'
	f = open(fn, 'r')
	lines = f.readlines()[1:-1]
	f.close()
	flines = [strictstrip(s) for s in lines]
	plines = sorted([strictstrip(s) for s in o.getJSON().split('\n')[1:-1]])
	ts = [tagliases[t] for t in tagliases.keys() if tagpositive(t, o.get('title'))]
	for t in tagkillz.keys():
		if t in ts and tagkillz[t] in ts:
			ts.remove(tagkillz[t])
	if ts:
		if not o.tags:
			o.tags = []
		for t in ts:
			if t not in o.tags:
				o.tags.append(t)
		# uncomment the following one line to overwrite all tags
		# o.tags = ts[:]
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
	f = open('tags.txt', 'r')
	for line in f.readlines():
		if not line.strip():
			continue
		if line.startswith('\t'):
			if line.strip().startswith('-'):
				if tagz[-1] not in tagkillz.keys():
					tagkillz[tagz[-1]] = []
				tagkillz[tagz[-1]].append(line.strip()[1:])
			else:
				tagliases[line.strip()] = tagz[-1]
		else:
			tagz.append(line.strip())
	f.close()
	for t in tagz:
		if t in tagliases.keys():
			print('ERROR: double definition of the tag', t)
		tagliases[t] = t
	print('{}: {} tags, {} venues, {} papers\n{}'.format(\
		C.purple('BibSLEIGH'),
		C.red(len(tagz)),
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
	print('{} files checked, {} ok, {} fixed, {} failed'.format(\
		C.bold(cx[0] + cx[1] + cx[2]),
		C.blue(cx[0]),
		C.yellow(cx[2]),
		C.red(cx[1])))
