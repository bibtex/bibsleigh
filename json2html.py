#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

from AST import *
from Fancy import colours

inputdir  = '../json'
outputdir = '../frontend'
sleigh = Sleigh(inputdir)
C = colours()

if __name__ == "__main__":
	cx = sum([v.numOfPapers() for v in sleigh.venues])
	cv = len(sleigh.venues)
	print('{} venues, {} papers'.format(C.purple('BibSLEIGH'), C.red(cv), C.red(cx)))
	f = open(outputdir+'/index.html', 'w')
	f.write(sleigh.getPage())
	f.close()
	for v in sleigh.venues:
		print(C.blue(v.getKey()), end=' => ')
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
			purekey = c.getKey().replace(v.getKey(),'').replace('-',' ').strip()
			print('{} [{}], '.format(purekey, C.yellow(len(c.papers))), end='')
		print()
