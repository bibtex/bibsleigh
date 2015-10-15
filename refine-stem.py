#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for stemming paper titles LRJ

import sys, os.path, glob
from fancy.ANSI import C
from lib.AST import Sleigh
from lib.JSON import parseJSON
from lib.NLP import string2words, ifApproved

# import stemming.porter2
import snowballstemmer
# from nltk.stem.snowball import SnowballStemmer

ienputdir = '../json'
n2f_name = '_name2file.json'
name2file = parseJSON(n2f_name) if os.path.exists(n2f_name) else {}
sleigh = Sleigh(ienputdir + '/corpus', name2file)
verbose = False
ALLSTEMS = set()

def guessYear(P):
	cys = [int(w) for w in P.split('-') if len(w) == 4 and w.isdigit()]
	if len(cys) == 1:
		return cys[0]
	else:
		j = sleigh.seekByKey(P)
		if 'year' in j.json.keys():
			return j.get('year')
		elif 'year' in dir(j):
			return j.year
		else:
			print('[ {} ] {}'.format(C.red('YEAR'), P))
			return 0

def checkon(fn, o):
	if not os.path.exists(fn) or os.path.isdir(fn):
		fn = fn + '.json'
	if 'title' not in o.json.keys():
		if verbose:
			print('No title in', o.getKey())
		return 1 # no title
	# check for a different language - to avoid stemming altogether
	if o.tags and ('german' in o.tags or 'french' in o.tags or 'portuguese' in o.tags):
		if 'stemmed' in o.json.keys():
			# if stemmed before marked foreign, remove this info
			del o.json['stemmed']
			F = open(fn, 'w')
			F.write(o.getJSON())
			F.close()
			return 2
		else:
			return 0
	changed = False
	### champion variant: snowballstemmer - runs in ~13.5s for 96027 titles
	stemmer = snowballstemmer.stemmer('english').stemWords
	### disregarded variant: snowballstemmer porter - considered outdated
	# stemmer = snowballstemmer.stemmer('porter').stemWords
	### disregarded variant: stemming - too slow, runs in ~33s for 96027 titles
	# stemmer = lambda xs: [stemming.porter2.stem(x) for x in xs]
	### disregarded variant: nltk - worse on verbs ending with -ze
	# stemmer3 = lambda xs: [SnowballStemmer("english").stem(x) for x in xs]
	### end variants
	stemmed = stemmer(string2words(o.get('title')))
	if '' in stemmed:
		print('“{}” is a title of {} and it has an empty word'.format(o.get('title'), C.red(o.getKey())))
		print(string2words(o.get('title')))
		print(stemmer(string2words(o.get('title'))))
	ALLSTEMS.update(stemmed)
	if o.get('stemmed') != stemmed:
		o.json['stemmed'] = stemmed
		changed = True
	if changed:
		F = open(fn, 'w')
		F.write(o.getJSON())
		F.close()
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

def two(n):
	if n < 10:
		return '0{}'.format(n)
	else:
		return '{}'.format(n)

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
	# stem ALL the papers!
	for v in sleigh.venues:
		for c in v.getConfs():
			for p in c.papers:
				cx[checkreport(p.filename, p)] += 1
	# write all stems
	listOfStems = sorted(filter(ifApproved, ALLSTEMS), key=lambda w: two(len(w)) + w)
	f = open(ienputdir + '/stems.json', 'w')
	f.write('[\n\t"' + '",\n\t"'.join(listOfStems) + '"\n]')
	f.close()
	print(C.red(len(ALLSTEMS)), 'stems found.')
	print('{} files checked, {} ok, {} fixed, {} failed'.format(\
		C.bold(cx[0] + cx[1] + cx[2]),
		C.blue(cx[0]),
		C.yellow(cx[2]),
		C.red(cx[1])))
