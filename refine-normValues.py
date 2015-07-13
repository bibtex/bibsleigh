#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for normalising values: numbers become proper integers, quotes — proper fancy ones, etc

import sys, os.path
from lib.AST import Sleigh
from fancy.ANSI import C
from lib.NLP import nrs, strictstrip

ienputdir = '../json'
n2f_name = '_name2file.json'
# name2file = parseJSON(n2f_name) if os.path.exists(n2f_name) else {}
sleigh = Sleigh(ienputdir + '/corpus', {})
verbose = False

def checkon(fn, o):
	if not os.path.exists(fn) or os.path.isdir(fn):
		fn = fn + '.json'
	# f = open(fn, 'r')
	# lines = f.readlines()[1:-1]
	# f.close()
	# flines = [strictstrip(s) for s in lines]
	plines = sorted([strictstrip(s) for s in o.getJSON().split('\n')[1:-1]])
	for k in o.json.keys():
		if (o.json['type'] == 'proceedings' and k == 'title') or\
		   (o.json['type'] == 'inproceedings' and k == 'booktitle'):
			# fix numbers
			for nr in nrs.keys():
				if o.json[k].find(' '+nr+' ') > -1:
					o.json[k] = o.json[k].replace(' '+nr+' ', ' '+nrs[nr]+' ')
		if isinstance(o.json[k], str):
			# add emdashes for fancier titles
			if k in ('title', 'booktitle'):
				o.json[k] = o.json[k].replace(' - ', ' — ')
			# normalised pages
			if k == 'pages':
				o.json[k] = o.json[k].replace('–', '-').replace('--', '-')
			# find numeric values, turn them into proper integers
			if o.json[k].isdigit():
				o.json[k] = int(o.json[k])
			# remove confix curlies
			elif o.json[k].startswith('{') and o.json[k].endswith('}'):
				o.json[k] = o.json[k][1:-1]
			# single quotes to double quotes
			elif o.json[k].find(" '") > -1 and o.json[k].find("' ") > -1:
				o.json[k] = o.json[k].replace(" '", ' "').replace("' ", '" ')
			elif o.json[k].find(" '") > -1 and o.json[k].endswith("'"):
				o.json[k] = o.json[k].replace(" '", ' "').replace("'", '"')
			elif o.json[k].find("' ") > -1 and o.json[k].startswith("'"):
				o.json[k] = o.json[k].replace("' ", '" ').replace("'", '"')
			# fancify quotes
			elif o.json[k].find(' "') > -1 and o.json[k].find('" ') > -1:
				o.json[k] = o.json[k].replace(' "', ' “').replace('" ', '” ')
			elif o.json[k].find(' "') > -1 and o.json[k].endswith('"'):
				o.json[k] = o.json[k].replace(' "', ' “').replace('"', '”')
			elif o.json[k].find('" ') > -1 and o.json[k].startswith('"'):
				o.json[k] = o.json[k].replace('" ', '” ').replace('"', '“')
			# the case of "Jr" vs "Jr."
			if k in ('author', 'editor') and o.json[k].endswith('Jr'):
				o.json[k] += '.'
		elif isinstance(o.json[k], list):
			# inline trivial lists
			if len(o.json[k]) == 1:
				o.json[k] = o.json[k][0]
			# remove DBLP disambiguation: we might later regret it
			# but the information can be always re-retrieved
			if k in ('author', 'editor'):
				nas = []
				for a in o.json[k]:
					ws = a.split(' ')
					if ws[-1].isdigit():
						ws = ws[:-1]
					nas.append(' '.join(ws))
				o.json[k] = nas
				# the case of "Jr" vs "Jr."
				o.json[k] = [a+'.' if a.endswith(' Jr') else a for a in o.json[k]]
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
