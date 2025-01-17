#!/c/Users/vadim/AppData/Local/Programs/Python/Python37-32/python
# -*- coding: utf-8 -*-
#
# a module for cross-checking information on people available from different sources

import sys, glob, os.path, json
from fancy.ANSI import C
from fancy.Latin import simpleLatin, dblpLatin, nodiaLatin
from lib.AST import Sleigh
from lib.JSON import parseJSON, jsonify
from lib.LP import listify, lastSlash

ienputdir = '../json'
n2f_name = '_name2file.json'
name2file = parseJSON(n2f_name) if os.path.exists(n2f_name) else {}
sleigh = Sleigh(ienputdir + '/corpus', name2file)
verbose = False
cx = {0: 0, 1: 0, 2: 0}
renameto = {}
dis = {}

def nomidnames(s):
	# ns = s.split(' ')
	# while len(ns) > 1 and len(ns[1]) == 2 and ns[1][0].isupper() and ns[1][1] == '.':
	# 	del ns[1]
	# return ' '.join(ns)
	s = s.replace('.', '. ').replace('  ', ' ')
	return ' '.join([n for n in s.split(' ') if len(n)!=2 or not n[0].isupper() or n[1]!='.'])

def fileify(s):
	return simpleLatin(s).replace('.', '').replace("'", '').replace(' ', '_')

def dblpify(s):
	# http://dblp.uni-trier.de/pers/hd/e/Elbaum:Sebastian_G=
	if s in dis.keys():
		return dis[s]
	if s.find(' ') < 0:
		print('[', C.red('NAME'), ']', 'Unconventional full name:', s)
		cx[1] += 1
		return dblpLatin(s)+':'
	ws = s.split(' ')
	i = -1
	if ws[i] in ('Jr', 'Jr.'):
		i -= 1
	sur = dblpLatin(' '.join(ws[i:]))
	rest = dblpLatin(' '.join(ws[:i])).replace(' ', '_')
	for c in ".'-":
		rest = rest.replace(c, '=')
	return sur+':'+rest

if __name__ == "__main__":
	print('Greetings, human.')
	verbose = sys.argv[-1] == '-v'
	# if not os.path.exists('_renameto.json'):
	# 	print('Run', C.blue('refine-aliases.py'), 'to build the aliasing/renaming relation and cache it.')
	# 	sys.exit(1)
	print('We start here.')
	# aka = parseJSON(ienputdir + '/aliases.json')
	dis = parseJSON(ienputdir + '/disambig.json')
	print('Parsed', ienputdir + '/disambig.json')
	renameto = parseJSON('_renameto.json')
	print('Parsed all JSONs.')
	sys.stdout.flush()
	# Data from the conferenceMetrics repo
	csv = []
	f = open('../conferenceMetrics/data/SE-conf-roles.csv', 'r', encoding='utf-8')
	for line in f.readlines():
		# Conference;Year;First Name;Last Name;Sex;Role
		csv.append(line.strip().split(';'))
	f.close()
	f = open('scrap-committees/scraped-by-grammarware.csv', 'r', encoding='utf-8')
	for line in f.readlines():
		csv.append(line.strip().split(';'))
	f.close()
	print('Parsed all CSVs.')
	sys.stdout.flush()
	# All known contributors
	people = {}
	for fn in glob.glob(ienputdir + '/people/*.json'):
		p = parseJSON(fn)
		# people.append(p)
		if 'name' not in p.keys():
			print('[', C.red('NOGO'), ']', 'No name in', fn)
			continue
		people[p['name']] = p
	print('Got all the known people.')
	print('{}: {} venues, {} papers\n{}'.format(\
		C.purple('BibSLEIGH'),
		C.red(len(sleigh.venues)),
		C.red(sleigh.numOfPapers()),
		C.purple('='*42)))
	# All people who ever contributed
	names = []
	sys.stdout.flush()
	for v in sleigh.venues:
		for c in v.getConfs():
			for p in c.papers:
				for k in ('author', 'editor'):
					if k in p.json.keys():
						names += [a for a in listify(p.json[k]) if a not in names]
	print('Got all the contributors.')
	sys.stdout.flush()
	# caching
	peoplekeys = people.keys()
	if os.path.exists('_established.json'):
		established = json.load(open('_established.json', 'r', encoding='utf-8'))
	else:
		established = {}
	print('Got all the established ones.')
	# print(people)
	CXread = len(people)
	for name in names:
		if name not in peoplekeys:
			p = {'name': name,\
				 'FILE': ienputdir + '/people/' + fileify(name) + '.json',\
				'dblp': dblpify(name)}
			people[p['name']] = p
	# flatten conferences for easy lookup
	knownConfs = []
	for v in sleigh.venues:
		for c in v.getConfs():
			knownConfs.append(c.getKey())
	# print(knownConfs)
	print(C.purple('BibSLEIGH flattened to {} entities'.format(len(knownConfs))))
	sys.stdout.flush()
	# compressed error output
	dunno = []
	# Conference;Year;First Name;Last Name;Sex;Role
	for line in csv:
		name = (line[2] + ' ' + line[3]).strip()
		if name in established.keys():
			name = established[name]
		if name in renameto.keys():
			print('[', C.yellow('ALIA'), ']', 'Treating', name, 'as', renameto[name])
			established[name] = renameto[name]
			name = renameto[name]
		if name not in peoplekeys:
			# not really needed, but just for the sake of wider applicability in the future
			ndl = nomidnames(nodiaLatin(name)).lower()
			f = None
			for k in peoplekeys:
				if nomidnames(nodiaLatin(k)).lower() == ndl:
					f = k
					break
			if not f:
				if name not in dunno:
					print('[', C.red('PERS'), ']', 'Unacquainted with', name)
					dunno.append(name)
				continue
			else:
				print('[', C.yellow('ALIA'), ']', 'Treating', name, 'as', k)
				established[name] = k
				name = k
		# renamed or not, here we come!
		if 'sex' not in people[name].keys() and line[4]:
			people[name]['sex'] = line[4]
		if 'roles' not in people[name].keys():
			people[name]['roles'] = []
		# slashes replaced by dashes (ESEC/FSE becomes ESEC-FSE)
		myconf = line[0].replace('/', '-') + '-' + line[1]
		if myconf not in knownConfs:
			if myconf not in dunno:
				print('[', C.red('CONF'), ']', 'No conference', myconf, 'found')
				dunno.append(myconf)
			continue
		if [myconf, line[5]] not in people[name]['roles']:
			people[name]['roles'].append([myconf, line[5]])
	# ensure fast load time next time
	# print(established)
	print('About to write the established relation.')
	sys.stdout.flush()
	f = open('_established.json', 'w', encoding='utf-8')
	f.write(json.dumps(established, sort_keys=True, separators=(',\n\t', ': '), ensure_ascii=False))
	f.close()
	print('\t', C.blue(CXread), 'people found in LRJs')
	print('\t', C.blue(len(people)), 'people properly specified')
	print('\t', C.blue(len(names)), 'people contributed to the corpus')
	print('\t', C.red(len(dunno)), 'people with too much info on')
	# should we build it?
	maken2f = not os.path.exists(n2f_name)
	if maken2f:
		name2file = {}
	for k in peoplekeys:
		p = people[k]
		if maken2f:
			name2file[k] = 'person/' + lastSlash(p['FILE']).replace('.json', '.html')
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
			f = open(p['FILE'], 'w', encoding='utf-8')
			del p['FILE']
			f.write(jsonify(p))
			f.close()
		else:
			print('How can that be?')
	# caching to be used later (in other scripts mostly)
	if maken2f:
		f = open(n2f_name, 'w', encoding='utf-8')
		f.write(json.dumps(name2file, sort_keys=True, separators=(',\n\t', ': '), ensure_ascii=False))
		f.close()
	cx[1] = len(dunno)
	print('{} people checked, {} ok, {} fixed, {} failed'.format(\
		C.bold(cx[0] + cx[1] + cx[2]),
		C.blue(cx[0]),
		C.yellow(cx[2]),
		C.red(cx[1])))
