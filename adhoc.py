#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for sorting the key-value pairs within each LRJ

import sys, os.path, glob
from fancy.ANSI import C
from lib.AST import Sleigh
from lib.JSON import parseJSON, jsonify, json2lines
from lib.NLP import strictstrip

ienputdir = '../json'
n2f_name = '_name2file.json'
name2file = parseJSON(n2f_name) if os.path.exists(n2f_name) else {}
sleigh = Sleigh(ienputdir + '/corpus', name2file)
verbose = False

def checkon(fn, o):
	if not os.path.exists(fn) or os.path.isdir(fn):
		fn = fn + '.json'
	# if o.getKey() not in ofInterest:
	# 	return 0
	flines = sorted(json2lines(o.getJSON().split('\n')))
	o.json['title'] = o.json['title'].replace('lambda', 'λ').replace('Lambda', 'λ')
	for mu in 'µ𝛍𝜇𝝁𝝻𝞵':
		o.json['title'] = o.json['title'].replace(mu, 'μ')
	for calc in ('-calculus', '-Calculus', ' calculus', ' Calculus', ' -calculus', ' -Calculus'):
		for mu in ('mu', 'Mu', '<i>μ</i>'):
			o.json['title'] = o.json['title'].replace(mu+calc, 'μ'+calc)
		for pi in ('pi', 'Pi'):
			o.json['title'] = o.json['title'].replace(pi+calc, 'π'+calc)
		o.json['title'] = o.json['title'].replace('λ-μ', 'λμ')
	# corner cases:
	# MICRO common representation language
	# synchrotron radiation x-ray MICROtomography
	# MICROkernel
	for corner in ('µCRL', 'SRµCT', 'µKernel'):
		o.json['title'] = o.json['title'].replace(corner.replace('µ', 'μ'), corner)
	for letter in ('alpha', 'beta', 'gamma', 'kappa', 'omega', 'sigma', 'varepsilon'):
		if o.json['title'].find(letter) > -1:
			print('Warning about', o.getKey(), ': "'+o.json['title']+'"')
	plines = sorted(json2lines(o.getJSON().split('\n')))
	if flines != plines:
		if 'stemmed' in o.json:
			del o.json['stemmed']
		f = open(fn, 'w')
		f.write(o.getJSON())
		f.close()
		return 2
	else:
		return 0

def checkreport(fn, o):
	statuses = (C.blue('PASS'), C.red('FAIL'), C.yellow('FIXD'))
	if isinstance(o, int):
		r = o
	else:
		r = checkon(fn, o)
	# non-verbose mode by default
	if verbose or r != 0:
		print('[ {} ] {}'.format(statuses[r], fn))
	return r

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
	for v in sleigh.venues:
		for c in v.getConfs():
			for p in c.papers:
				cx[checkreport(p.filename, p)] += 1
	print('{} files checked, {} ok, {} fixed, {} failed'.format(\
		C.bold(cx[0] + cx[1] + cx[2]),
		C.blue(cx[0]),
		C.yellow(cx[2]),
		C.red(cx[1])))
