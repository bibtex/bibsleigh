#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import glob
from Templates import uberHTML
from AST import *

# import os, sys, glob
# from template import uberHTML, confHTML, bibHTML, hyper_series
# from supported import supported

inputdir  = '../json'
outputdir = '../frontend'

if __name__ == "__main__":
	venues = []
	for d in glob.glob(inputdir+'/*'):
		venues.append(Venue(d, inputdir))
	cx = sum([v.numOfPapers() for v in venues])
	print('{} venues, {} papers'.format(len(venues), cx))
	f = open(outputdir+'/index.html', 'w')
	f.write(uberHTML.format(cx, '\n'.join([v.getItem() for v in venues])))
	f.close()
	for v in venues:
		print(v.getKey(), end=' => ')
		f = open(outputdir+'/'+v.getKey()+'.html', 'w')
		f.write(v.getPage())
		f.close()
		for c in v.getConfs():
			f = open(outputdir+'/'+c.getKey()+'.html', 'w')
			f.write(c.getPage())
			f.close()
			for p in c.papers:
				# print(p.json)
				f = open(outputdir+'/'+p.getKey()+'.html', 'w')
				f.write(p.getPage())
				f.close()
			print('{} [{}], '.format(c.getKey(), len(c.papers)), end='')
		print()
