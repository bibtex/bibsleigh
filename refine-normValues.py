#!/c/Users/vadim/AppData/Local/Programs/Python/Python35/python
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
lookat = []

def checkon(fn, o):
	if not os.path.exists(fn) or os.path.isdir(fn):
		fn = fn + '.json'
	plines = sorted([strictstrip(s) for s in o.getJSON().split('\n')[1:-1]])
	for k in o.json.keys():
		if 'type' not in o.json.keys():
			print('TERRIBLE',o.getKey())
		if (o.json['type'] == 'proceedings' and k == 'title') or\
		   (o.json['type'] == 'inproceedings' and k == 'booktitle'):
			# fix numbers
			for nr in nrs.keys():
				if o.json[k].find(' '+nr+' ') > -1:
					o.json[k] = o.json[k].replace(' '+nr+' ', ' '+nrs[nr]+' ')
		if isinstance(o.json[k], str):
			# add emdashes for fancier titles
			if k in ('title', 'booktitle'):
				o.json[k] = o.json[k].replace(' - ', ' — ').replace(' -- ', ' — ')
				# Nice heuristic to run from time to time, but reports too much
				# on stuff like “eXtreme” and “jPET”
				# if o.json[k][0].islower():
				# 	print('[ {} ] {}: {} {}'.format(C.red('LOOK'), o.getKey(), 'title is', o.get('title')))
			# normalised pages
			if k == 'pages':
				o.json[k] = o.json[k].replace('–', '-').replace('--', '-').replace('−', '-')
			# double spaces
			if o.json[k].find('  ') > -1:
				o.json[k] = o.json[k].replace('  ', ' ').strip()
			# find numeric values, turn them into proper integers
			if o.json[k].isdigit():
				o.json[k] = int(o.json[k])
				continue
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
			# fancify bland quotes
			elif o.json[k].find(' "') > -1 and o.json[k].find('" ') > -1:
				o.json[k] = o.json[k].replace(' "', ' “').replace('" ', '” ')
			elif o.json[k].find(' "') > -1 and o.json[k].endswith('"'):
				o.json[k] = o.json[k].replace(' "', ' “').replace('"', '”')
			elif o.json[k].find('" ') > -1 and o.json[k].startswith('"'):
				o.json[k] = o.json[k].replace('" ', '” ').replace('"', '“')
			# fancify LaTeX quotes
			elif o.json[k].find(' ``') > -1 and o.json[k].find("'' ") > -1:
				o.json[k] = o.json[k].replace("'' ", '” ').replace(' ``', ' “')
			elif o.json[k].find(' ``') > -1 and o.json[k].endswith("''"):
				o.json[k] = o.json[k].replace("''", '”').replace(' ``', ' “')
			elif o.json[k].find("'' ") > -1 and o.json[k].startswith('``'):
				o.json[k] = o.json[k].replace("'' ", '” ').replace('``', '“')
			elif o.json[k].startswith('``') and o.json[k].endswith("''"):
				o.json[k] = '“' + o.json[k][2:-2] + '”'
			# plural possessive
			elif o.json[k].find("'s") > -1:
				o.json[k] = o.json[k].replace("'s", '’s')
			elif o.json[k].find("s' ") > -1:
				o.json[k] = o.json[k].replace("s'", 's’')
			# contractions
			elif o.json[k].find("n't") > -1:
				o.json[k] = o.json[k].replace("n't", 'n’t')
			# the case of "Jr" vs "Jr."
			if k in ('author', 'editor') and o.json[k].endswith('Jr'):
				o.json[k] += '.'
			# TODO: report remaining suspicious activity
			for c in '`"\'': # ’ is ok
				if c in o.json[k] and k not in ('author', 'editor'):
					print('[ {} ] {}: {} is “{}”'.format(C.red('LOOK'), o.getKey(), k, o.json[k]))
					lookat.append(o.filename)
		elif isinstance(o.json[k], list):
			# inline trivial lists
			if len(o.json[k]) == 1:
				o.json[k] = o.json[k][0]
			# inline hidden trivial lists
			if len(o.json[k]) == 2 and o.json[k][0] == o.json[k][1] \
			and k not in ('stemmed', 'tag', 'tagged'):
				o.json[k] = o.json[k][0]
			# unless it’s 'tagged'
			if k == 'tagged' and not isinstance(o.json[k][0], list):
				o.json[k] = [o.json[k]]
			# remove DBLP disambiguation: we might later regret it
			# but the information can be always re-retrieved
			if k in ('author', 'editor'):
				nas = []
				for a in o.json[k]:
					# double spaces
					if a.find('  ') > -1:
						a = a.replace('  ', ' ').strip()
					ws = a.split(' ')
					if ws[-1].isdigit():
						ws = ws[:-1]
					nas.append(' '.join(ws))
				o.json[k] = nas
				# the case of "Jr" vs "Jr."
				o.json[k] = [a+'.' if a.endswith(' Jr') else a for a in o.json[k]]
	nlines = sorted([strictstrip(s) for s in o.getJSON().split('\n')[1:-1]])
	if plines != nlines:
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
	for f in lookat:
		print('\t'+f)
