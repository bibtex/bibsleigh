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

def sdistance(x1, x2):
	return str(distance(x1, x2)).replace('.', ',')

def distance(x1, x2):
	return sqrt(sum([(x1[jj]-x2[jj])**2 for jj in range(0, len(x1))]))

# NB: some clustering/visualisation code based on http://brandonrose.org/clustering
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
	UberCols = set()
	vocs = {b.getKey():b.json['vocabulary'] \
		for v in sleigh.venues \
		for b in v.getBrands() \
		if 'vocabulary' in b.json \
		if len(b.json['vocabulary']) > 10}
	for vkey in vocs:
		UberDict.update(vocs[vkey].keys())
	# collocations are not quantified!
	cols = {b.getKey():[col for col in b.json['collocations'] if b.json['collocations'][col] > 1] \
		for v in sleigh.venues \
		for b in v.getBrands() \
		if 'collocations' in b.json}
	for vkey in cols:
		UberCols.update(cols[vkey])
	print('The überdictionary has', \
		C.red(len(UberDict)), 'words and', \
		C.red(len(UberCols)), 'collocations.')
	AllWords = sorted(UberDict)
	AllColls = sorted(UberCols)

	##### first, for vocabularies
	# form vectors from dictionaries
	vecs = {vkey:[vocs[vkey][w] for w in AllWords] for vkey in vocs}
	print('Vectors for vocabularies formed.')
	# how far is each from everything else?
	far = {vkey:sum([distance(vecs[vkey], vecs[vk2]) for vk2 in vocs])/len(vocs) for vkey in vocs}
	# print(far)
	vockeys = sorted(vocs.keys(), key=lambda z: far[z])
	# print(vockeys)
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
	plt.savefig('clusters-voc.png', dpi=200)
	print('Figure plotted.')

	##### now, for n-gram-sets
	# form vectors - remember: not quantified!
	vecs = {vkey:[w in cols[vkey] for w in AllColls] for vkey in cols}
	print('Vectors for n-gram-sets formed.')
	# how far is each from everything else?
	# far = {vkey:sum([distance(vecs[vkey], vecs[vk2]) for vk2 in cols])/len(vocs) for vkey in cols}
	# print(far)
	colkeys = sorted(cols.keys())#, key=lambda z: far[z])
	# print(colkeys)
	distanceMatrix = []
	for vk1 in colkeys:
		distanceMatrix.append([])
		for vk2 in colkeys:
			distanceMatrix[-1].append(distance(vecs[vk1], vecs[vk2]))
	minD = min([min([v for v in distanceMatrix[i] if v > 0]) for i in range(0, len(distanceMatrix))])
	maxD = max([max(distanceMatrix[i]) for i in range(0, len(distanceMatrix))])
	print('Distance matrix computed, values from {} to {}'.format(minD, maxD))
	s = ' ; ' + ';'.join(colkeys) + '\n'
	colidx = range(0, len(colkeys))
	for i in colidx:
		s += colkeys[i]+' ; '+';'.join([str(distanceMatrix[i][j]) for j in colidx]) +'\n'
	f = open('colsim.csv', 'w')
	f.write(s)
	f.close()
	print('Distance matrix saved as CSV.')
	#define the linkage_matrix using ward clustering pre-computed distances
	linkage_matrix = ward(distanceMatrix)
	fig, ax = plt.subplots(figsize=(15, 20)) # set size
	ax = dendrogram(linkage_matrix, \
		orientation="right", \
		labels=['{} ({})'.format(key, len(cols[key])) for key in colkeys])
	plt.tick_params(\
	    axis='x',          # changes apply to the x-axis
	    which='both',      # both major and minor ticks are affected
	    bottom='off',      # ticks along the bottom edge are off
	    top='off',         # ticks along the top edge are off
	    labelbottom='off')
	plt.tight_layout() #show plot with tight layout
	plt.savefig('clusters-col.png', dpi=200)
	print('Figure plotted.')

	print('{} files checked, {} ok, {} fixed, {} failed'.format(\
		C.bold(cx[0] + cx[1] + cx[2]),
		C.blue(cx[0]),
		C.yellow(cx[2]),
		C.red(cx[1])))
