#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for exporting LRJs to the HTML frontpages

import Fancy, AST, Templates, sys, os
sys.path.append(os.getcwd()+'/../beauty')

ienputdir = '../json'
outputdir = '../frontend'
sleigh = AST.Sleigh(ienputdir + '/corpus')
C = Fancy.colours()

if __name__ == "__main__":
	print('{}: {} venues, {} papers\n{}'.format(\
		C.purple('BibSLEIGH'),
		C.red(len(sleigh.venues)),
		C.red(sleigh.numOfPapers()),
		C.purple('='*42)))
	f = open(outputdir+'/index.html', 'w')
	f.write(sleigh.getPage())
	f.close()
	for v in sleigh.venues:
		r = C.blue(v.getKey()) + ' => '
		f = open(outputdir+'/'+v.getKey()+'.html', 'w')
		f.write(v.getPage())
		f.close()
		for c in v.getConfs():
			f = open(outputdir+'/'+c.getKey()+'.html', 'w')
			f.write(c.getPage())
			f.close()
			for p in c.papers:
				f = open(outputdir+'/'+p.getKey()+'.html', 'w')
				f.write(p.getPage())
				f.close()
			purekey = c.getKey().replace(v.getKey(), '').replace('-', ' ').strip()
			r += '{} [{}], '.format(purekey, C.yellow(len(c.papers)))
		print(r)
	print('{}\nDone with {} venues, {} papers.'.format(\
		C.purple('='*42),
		C.red(len(sleigh.venues)),
		C.red(sleigh.numOfPapers())))
