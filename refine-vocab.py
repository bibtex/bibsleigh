#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for dealing with vocabularies

import sys, os.path, glob
from fancy.ANSI import C
from lib.AST import Sleigh
from lib.JSON import parseJSON, jsonify, json2lines
from lib.NLP import strictstrip
from math import sqrt

ienputdir = '../json'
sleigh = Sleigh(ienputdir + '/corpus', {})
verbose = False

def checkon(fn, o):
	if not os.path.exists(fn) or os.path.isdir(fn):
		fn = fn + '.json'
	# print('Checking', fn, '...')
	# f = open(fn, 'r')
	# lines = f.readlines()[1:-1]
	# f.close()
	# flines = json2lines(lines)
	plines = sorted(json2lines(o.getJSON().split('\n')))
	flines = sorted(json2lines(o.getJSON().split('\n')))
	if flines != plines:
		f1 = [line for line in flines if line not in plines]
		f2 = [line for line in plines if line not in flines]
		if f1 or f2:
			if verbose:
				print('∆:', f1, 'vs', f2)
			print('F-lines:', '\n'.join(flines))
			print('P-lines:', '\n'.join(plines))
			return 1
		else:
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

def sdistance(x1, x2):
	return str(distance(x1, x2)).replace('.', ',')

def distance(x1, x2):
	return sqrt(sum([(x1[i]-x2[i])**2 for i in range(0, len(x1))]))

if __name__ == "__main__":
	verbose = sys.argv[-1] == '-v'
	peoplez = glob.glob(ienputdir + '/people/*.json')
	print('{}: {} venues, {} papers by {} people\n{}'.format(\
		C.purple('BibSLEIGH'),
		C.red(len(sleigh.venues)),
		C.red(sleigh.numOfPapers()),
		C.red(len(peoplez)),
		C.purple('='*42)))
	cx = {0: 0, 1: 0, 2: 0}
	# we need to know all the words we have
	UberDict = set()
	vocs = {b.getKey():b.json['vocabulary'].keys() \
		for v in sleigh.venues for b in v.getBrands() if 'vocabulary' in b.json}
	for vkey in vocs:
		UberDict.update(vocs[vkey])
	print('The überdictionary has', C.red(len(UberDict)), 'words.')
	AllWords = sorted(UberDict)
	# form vectors from dictionaries
	vecs = {vkey:[w in vocs[vkey] for w in AllWords] for vkey in vocs}
	print('Vectors formed.')
	# how far is each from everything else?
	far = {vkey:sum([distance(vecs[vkey], vecs[vk2]) for vk2 in vocs])/len(vocs) for vkey in vocs}
	print(far)
	vockeys = sorted(vocs.keys(), key=lambda z: far[z])
	print(vockeys)
	s = ' ; ' + ';'.join(vockeys) + '\n'
	for vkey in vockeys:
		s += vkey + ' ; ' + ';'.join([sdistance(vecs[vkey], vecs[vk2]) for vk2 in vockeys]) + '\n'
	f = open('vocsim.csv', 'w')
	f.write(s)
	f.close()
	# for v in sleigh.venues:
	# 	for b in v.getBrands():
	# 		cx[checkreport(b.filename, b)] += 1
	print('{} files checked, {} ok, {} fixed, {} failed'.format(\
		C.bold(cx[0] + cx[1] + cx[2]),
		C.blue(cx[0]),
		C.yellow(cx[2]),
		C.red(cx[1])))
