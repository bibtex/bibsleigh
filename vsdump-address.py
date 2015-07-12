#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for deriving location values from the DBLP XML dump

import sys, os.path
from lib.AST import Sleigh
from fancy.ANSI import C
from lib.NLP import nrs, strictstrip
import xml.etree.cElementTree as ET
# from lib.JSON import jsonify
# from lib.JSON import parseJSON
import json
from fancy.Countries import knownCountries

ienputdir = '../json'
sleigh = Sleigh(ienputdir + '/corpus')
verbose = False
procs = {}

# knownCountries = ('USA', 'Australia', 'China', 'Canada', 'UK', 'Taiwan', 'Japan',
# 'United Kingdom',
# 'France', 'Switzerland', 'Germany', 'Spain', 'Czech Republic', 'The Netherlands',
# 'Cyprus', 'Italy', 'Romania', 'Estonia', 'Portugal', 'Netherlands', 'Hungary',
# 'Belgium', 'Ireland', 'Greece', 'Finland', 'Norway')

def checkon(fn, o):
	if 'dblpkey' not in o.json.keys():
		print('[ {} ] {}'.format(C.red('DONT'), 'DBLP key not found on the entry'))
		return 1
	mykey = o.get('dblpkey')
	if mykey not in procs.keys():
		print('[ {} ] {}'.format(C.red('DONT'), 'DBLP key not found in the dump'))
		return 1
	title = procs[mykey]
	if title.endswith('.'):
		title = title[:-1]
	ws = title.replace(' - ', ', ').split(', ')
	for country in knownCountries:
		if country in ws:
			print('[ {} ] {}'.format(C.blue('KNOW'), country))
			return 0
	print('[ {} ] {}'.format(C.yellow('????'), title))
	return 2
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
	# now read in the proceedings entries from the dump
	# parser = ET.XMLParser(encoding="utf-8")
	# for event, elem in ET.iterparse('../dblp.xml', events=("end",), parser=parser):
	# 	if elem.tag == 'proceedings':
	# 		dblpkey = elem.attrib['key']
	# 		# <title>Constraint Programming: Basics and Trends, Châtillon Spring School, Châtillon-sur-Seine, France, May 16 - 20, 1994, Selected Papers</title>
	# 		title = elem.findtext('title')
	# 		# procs.append(elem)
	# 		procs[dblpkey] = title
	# f = open('procs.json', 'w')
	# f.write(json.dumps(procs, sort_keys=True, separators=(',\n\t', ': ')))
	# f.close()
	procs = json.load(open('procs.json', 'r'))
	print('{} proceedings volumes found.'.format(len(procs)))
	for v in sleigh.venues:
		for c in v.getConfs():
			cx[checkreport(c.filename, c)] += 1
			# for p in c.papers:
			# 	cx[checkreport(p.filename, p)] += 1
	print('{} files checked, {} ok, {} fixed, {} failed'.format(\
		C.bold(cx[0] + cx[1] + cx[2]),
		C.blue(cx[0]),
		C.yellow(cx[2]),
		C.red(cx[1])))
