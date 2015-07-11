#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for cross-checking information on people available from different sources

import sys, glob, os.path
from fancy.ANSI import C
from fancy.Latin import simpleLatin, dblpLatin
from lib.AST import Sleigh
from lib.JSON import parseJSON, jsonify
from lib.LP import listify

ienputdir = '../json'
sleigh = Sleigh(ienputdir + '/corpus')
verbose = False
cx = {0: 0, 1: 0, 2: 0}

def fileify(s):
	return simpleLatin(s).replace('.', '').replace("'", '').replace(' ', '_')

def dblpify(s):
	# http://dblp.uni-trier.de/pers/hd/e/Elbaum:Sebastian_G=
	if s.find(' ') < 0:
		print('[', C.red('NAME'), ']', 'Unconventional full name:', s)
		cx[1] += 1
		return s
	sur = s[s.rindex(' ')+1:]
	rest = dblpLatin(s[:s.rindex(' ')]).replace(' ', '_').replace('.', '=').replace("'", '=')
	return sur+':'+rest

if __name__ == "__main__":
	verbose = sys.argv[-1] == '-v'
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
	# flatten conferences for easy lookup
	# confByKey = {}
	knownConfs = []
	for v in sleigh.venues:
		for c in v.getConfs():
			# confByKey[c.getKey()] = c
			knownConfs.append(c.getKey())
	print(knownConfs)
	# compressed error output
	dunno = []
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
			if name in dunno:
				continue
			print('[', C.red('PERS'), ']', 'Unacquainted with', name)
			dunno.append(name)
		else:
			if 'sex' not in people[jdx].keys():
				people[jdx]['sex'] = line[4]
			if 'roles' not in people[jdx].keys():
				people[jdx]['roles'] = []
			# slashes replaced by dashes (ESEC/FSE becomes ESEC-FSE)
			myconf = line[0].replace('/', '-') + '-' + line[1]
			if myconf not in knownConfs:
				print('[', C.red('CONF'), ']', 'No conference', myconf, 'found')
				continue
			if [myconf, line[5]] not in people[jdx]['roles']:
				people[jdx]['roles'].append([myconf, line[5]])
	print('\t', C.blue(len(people)), 'people properly specified')
	print('\t', C.blue(len(names)), 'people contributed to the corpus')
	print('\t', C.red(len(dunno)), 'people with too much info on')
	for p in people:
		if p['FILE']:
			if os.path.exists(p['FILE']):
				cur = parseJSON(p['FILE'])
				if cur == p:
					cx[0] += 1
					if verbose:
						print('[', C.green('FIXD'), ']', p['name'])
					continue
			print('[', C.yellow('FIXD'), ']', p['name'])
			cx[2] += 1
			f = open(p['FILE'], 'w')
			del p['FILE']
			f.write(jsonify(p))
			f.close()
		else:
			print('How can that be?')
	cx[1] = len(dunno)
	print('{} people checked, {} ok, {} fixed, {} failed'.format(\
		C.bold(cx[0] + cx[1] + cx[2]),
		C.blue(cx[0]),
		C.yellow(cx[2]),
		C.red(cx[1])))
