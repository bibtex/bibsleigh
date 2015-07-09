#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for normalising values: numbers become proper integers, quotes — proper fancy ones, etc

import sys, glob
from fancy.ANSI import C
from fancy.Latin import diacritics
from lib.AST import Sleigh
from lib.JSON import parseJSON, jsonify
from lib.LP import listify

ienputdir = '../json'
sleigh = Sleigh(ienputdir + '/corpus')
verbose = False

def fileify(s):
	for d in diacritics.keys():
		s = s.replace(d, diacritics[d])
	return s.replace('.', '').replace(' ', '_')

def dblpify(s):
	# http://dblp.uni-trier.de/pers/hd/e/Elbaum:Sebastian_G=
	if s.find(' ') < 0:
		print('Unknown:', s)
		return s
	sur = s[s.rindex(' ')+1:]
	rest = s[:s.rindex(' ')].replace(' ', '_').replace('.', '=')
	return sur+':'+rest

if __name__ == "__main__":
	if len(sys.argv) > 1:
		verbose = sys.argv[1] == '-v'
	# Data from the conferenceMetrics repo
	csv = []
	f = open('../conferenceMetrics/data/SE-conf-roles.csv', 'r')
	for line in f.readlines():
		# Conference;Year;First Name;Last Name;Sex;Role
		csv.append(line.strip().split(';'))
	f.close()
	# All known contributors
	people = []
	for fn in glob.glob(ienputdir + '/people/*.json'):
		p = parseJSON(fn)
		people.append(p)
	print('{}: {} venues, {} papers\n{}'.format(\
		C.purple('BibSLEIGH'),
		C.red(len(sleigh.venues)),
		C.red(sleigh.numOfPapers()),
		C.purple('='*42)))
	cx = {0: 0, 1: 0, 2: 0}
	# All people who ever contributed
	names = []
	for v in sleigh.venues:
		for c in v.getConfs():
			for p in c.papers:
				for k in ('author', 'editor'):
					if k in p.json.keys():
						names += [a for a in listify(p.json[k]) if a not in names]
	# print(people)
	for i, name in enumerate(names):
		idx = -1
		for p in people:
			if p['name'] == name:
				idx = i
				break
		if idx == -1:
			p = {'name': name,\
				 'FILE': ienputdir + '/people/' + fileify(name) + '.json',\
				'dblp': dblpify(name)}
			people.append(p)
	# Conference;Year;First Name;Last Name;Sex;Role
	for i, line in enumerate(csv):
		idx = jdx = -1
		name = line[2] + ' ' + line[3]
		for j, p in enumerate(people):
			if p['name'] == name:
				idx = i
				jdx = j
				break
		if idx < 0 or jdx < 0:
			print('Don’t know no', name)
		else:
			if 'sex' not in people[jdx].keys():
				people[jdx]['sex'] = line[4]
			if 'roles' not in people[jdx].keys():
				people[jdx]['roles'] = []
			# excessive!
			if [line[0], line[1], line[5]] not in people[jdx]['roles']:
				people[jdx]['roles'].append([line[0], line[1], line[5]])
	print('\t{} people properly specified,\n\t{} people contributed to the corpus'.format(\
		C.red(len(people)),
		C.red(len(names))))
	for p in people:
		if p['FILE']:
			f = open(p['FILE'], 'w')
			del p['FILE']
			f.write(jsonify(p))
			f.close()
		else:
			print('How can that be?')
	print('{} files checked, {} ok, {} fixed, {} failed'.format(\
		C.bold(cx[0] + cx[1] + cx[2]),
		C.blue(cx[0]),
		C.yellow(cx[2]),
		C.red(cx[1])))
