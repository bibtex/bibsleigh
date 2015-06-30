#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import sys, os
sys.path.append(os.getcwd()+'/../engine')
import Fancy, AST, os.path

ienputdir = '../json'
sleigh = AST.Sleigh(ienputdir)
C = Fancy.colours()
verbose = False

nrs = {'1st': 'First', '2nd': 'Second', '3rd': 'Third', '4th': 'Fourth',
'5th': 'Fifth', '6th': 'Sixth', '7th': 'Seventh', '8th': 'Eighth',
'9th': 'Ninth', 'Tenth': '10th', 'Eleventh': '11th', 'Twelfth': '12th'}

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
	for k in o.json.keys():
		if (o.json['type'] == 'proceedings' and k == 'title') or\
		   (o.json['type'] == 'inproceedings' and k == 'booktitle'):
			for nr in nrs.keys():
				if o.json[k].find(' '+nr+' ') > -1:
					o.json[k] = o.json[k].replace(' '+nr+' ', ' '+nrs[nr]+' ')
		elif isinstance(o.json[k], str):
			# find numeric values, turn them into proper integers
			if o.json[k].isdigit():
				o.json[k] = int(o.json[k])
			# remove confix curlies
			elif o.json[k].startswith('{') and o.json[k].endswith('}'):
				o.json[k] = o.json[k][1:-1]
			# fancify quotes
			elif o.json[k].find(' "') > -1 and o.json[k].find('" ') > -1:
				o.json[k] = o.json[k].replace(' "', ' “').replace('" ', '” ')
			elif o.json[k].find(' "') > -1 and o.json[k].endswith('"'):
				o.json[k] = o.json[k].replace(' "', ' “').replace('"', '”')
			elif o.json[k].find('" ') > -1 and o.json[k].startswith('"'):
				o.json[k] = o.json[k].replace('" ', '” ').replace('"', '“')
		elif isinstance(o.json[k], list):
			# inline trivial lists
			if len(o.json[k]) == 1:
				o.json[k] = o.json[k][0]
	nlines = sorted([strictstrip(s) for s in o.getJSON().split('\n')[1:-1]])
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
