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
# import cluster
from scipy.cluster.hierarchy import ward, dendrogram
import matplotlib.pyplot as plt
import matplotlib as mpl

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
	# print('Asked about the distance between', x1, 'and', x2)
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
	vocs = {b.getKey():b.json['vocabulary'] \
		for v in sleigh.venues \
		for b in v.getBrands() \
		if 'vocabulary' in b.json \
		if len(b.json['vocabulary']) > 10}
	for vkey in vocs:
		UberDict.update(vocs[vkey].keys())
	print('The überdictionary has', C.red(len(UberDict)), 'words.')
	AllWords = sorted(UberDict)
	# form vectors from dictionaries
	vecs = {vkey:[vocs[vkey][w] for w in AllWords] for vkey in vocs}
	print('Vectors formed.')
	# how far is each from everything else?
	far = {vkey:sum([distance(vecs[vkey], vecs[vk2]) for vk2 in vocs])/len(vocs) for vkey in vocs}
	# print(far)
	vockeys = sorted(vocs.keys(), key=lambda z: far[z])
	print(vockeys)
	distanceMatrix = []
	for vk1 in vockeys:
		distanceMatrix.append([])
		for vk2 in vockeys:
			distanceMatrix[-1].append(distance(vecs[vk1], vecs[vk2]))
	minD = min([min([v for v in distanceMatrix[i] if v > 0]) for i in range(0, len(distanceMatrix))])
	maxD = max([max(distanceMatrix[i]) for i in range(0, len(distanceMatrix))])
	print('Distance matrix computed, values from {} to {}'.format(minD, maxD))
	s = ' ; ' + ';'.join(vockeys) + '\n'
	vocidx = range(0, len(vockeys))
	for i in vocidx:
		# s += vkey + ' ; ' + ';'.join([sdistance(vecs[vkey], vecs[vk2]) for vk2 in vockeys]) + '\n'
		s += vockeys[i]+' ; '+';'.join([str(distanceMatrix[i][j]) for j in vocidx]) +'\n'
	f = open('vocsim.csv', 'w')
	f.write(s)
	f.close()
	print('Distance matrix saved as CSV.')
	# cs = cluster.HierarchicalClustering(vocidx, lambda vk1, vk2: distanceMatrix[vk1][vk2])
	# print(cs.getlevel(10))

	#define the linkage_matrix using ward clustering pre-computed distances
	linkage_matrix = ward(distanceMatrix)
	fig, ax = plt.subplots(figsize=(15, 20)) # set size
	ax = dendrogram(linkage_matrix, \
		orientation="right", \
		labels=['{} ({})'.format(key, len(vocs[key])) for key in vockeys])

	plt.tick_params(\
	    axis='x',          # changes apply to the x-axis
	    which='both',      # both major and minor ticks are affected
	    bottom='off',      # ticks along the bottom edge are off
	    top='off',         # ticks along the top edge are off
	    labelbottom='off')

	plt.tight_layout() #show plot with tight layout
	plt.savefig('bibsleigh_clusters.png', dpi=200) #save figure as ward_clusters
	# for v in sleigh.venues:
	# 	for b in v.getBrands():
	# 		cx[checkreport(b.filename, b)] += 1
	print('Figure plotted.')
	print('{} files checked, {} ok, {} fixed, {} failed'.format(\
		C.bold(cx[0] + cx[1] + cx[2]),
		C.blue(cx[0]),
		C.yellow(cx[2]),
		C.red(cx[1])))
