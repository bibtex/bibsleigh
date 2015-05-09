#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import os, sys, glob
from template import uberHTML, confHTML, bibHTML, hyper_series
from supported import supported

def last(x):
	return x.split('/')[-1].replace('.json', '')

def parent(x):
	return x[:x.rfind('/')]
	# return x.split('/')[-1].replace('.json', '')

def parseJSON(fn):
	dct = {}
	f = open(fn, 'r')
	for line in f.readlines():
		line = line.strip()
		if line in ('{', '}', ''):
			continue
		perq = line.split('"')
		if len(perq) == 5:
			dct[perq[1]] = perq[3]
		elif len(perq) == 3 and perq[1] == 'year':
			dct[perq[1]] = int(perq[-1][2:-1])
		elif len(perq) > 5:
			dct[perq[1]] = [x for x in perq[3:-1] if x != ', ']
		else:
			print('Skipped line', line, 'in', fn)
	f.close()
	dct['FILE'] = fn
	return dct

def traverseDir(d, s, b):
	for f in glob.glob(d+'/*'):
		cnf = last(f)
		if os.path.isdir(f):
			# print('{}{} conference found'.format(s, cnf))
			b[f] = {'FILE':f}
			traverseDir(f, s+'\t', b)
		else:
			# print('{}{} file found as a parent of {}'.format(s, cnf, parent(cnf)))
			b[f] = parseJSON(f)

if __name__ == "__main__":
	GCX = 0
	# allconfs = []
	bib = {}
	traverseDir('bibdata', '', bib)
	print('[Total: {} entries]'.format(len(bib)))
	print('-'*100)
	for k in bib.keys():
		j = bib[k]
		pr = 1 if parent(k) in bib.keys() else 0
		children = [kk for kk in bib.keys() if kk.startswith(k) and kk[len(k):] != '' and kk[len(k)+1:].find('/') < 0]
		# children = [kk[len(k)+1:].find('/')<0 for kk in bib.keys() if kk.startswith(k) and kk[len(k):] != '']
		types = [bib[x]['type'] for x in children if 'type' in bib[x].keys()]
		print('{}: {} parents, {} children, types {}'.format(k, pr, len(children), types))

		if pr == 0:
			# TODO: save for index.html
			pass
