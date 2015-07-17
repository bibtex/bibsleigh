#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for exporting LRJs to the HTML frontpages

import os.path, glob
from fancy.ANSI import C
from fancy.Templates import aboutHTML
from lib.AST import Sleigh
from lib.JSON import parseJSON

ienputdir = '../json'
outputdir = '../frontend'
n2f_name = '_name2file.json'
name2file = parseJSON(n2f_name) if os.path.exists(n2f_name) else {}
sleigh = Sleigh(ienputdir + '/corpus', name2file)

if __name__ == "__main__":
	print('{}: {} venues, {} papers\n{}'.format(\
		C.purple('BibSLEIGH'),
		C.red(len(sleigh.venues)),
		C.red(sleigh.numOfPapers()),
		C.purple('='*42)))
	# generate the index
	f = open(outputdir+'/index.html', 'w')
	f.write(sleigh.getPage())
	f.close()
	# generate all individual pages
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
	# generate the icon lineup
	icons = []
	linked = []
	for png in glob.glob(outputdir + '/stuff/*.png'):
		pure = png.split('/')[-1].split('.')[0]
		if pure.startswith('a-') or pure.startswith('p-') or pure.startswith('ico-')\
		or pure in ('cc-by', 'xhtml', 'css', 'open-knowledge', 'edit'):
			continue
		# the MSR logo is not redrawn (yet)
		if pure == 'msr':
			continue
		canlink = glob.glob(outputdir + '/' + pure.upper().replace('+', '') + '*.html')
		if canlink:
			canlink = sorted(canlink, key=len)
			# the case of ESEC-* vs ESEC-FSE
			i = 0
			while canlink[i] in linked:
				i += 1
			pic = '<a href="{}"><img class="abc" src="{}" alt="{}"/></a>'.format(\
				canlink[i],
				png.replace(outputdir + '/', ''),
				png.split('/')[-1].split('.')[0])
			linked.append(canlink[i])
		else:
			print('No link for', pure)
			pic = '<img class="abc" src="{}" alt="{}"/>'.format(\
				png.replace(outputdir + '/', ''),
				png.split('/')[-1].split('.')[0])
		icons.append(pic)
	f = open(outputdir+'/about.html', 'w')
	f.write(aboutHTML.format(len(icons), '<div class="minibar">' + '\n'.join(icons) + '</div>'))
	f.close()
	print('{}\nDone with {} venues, {} papers.'.format(\
		C.purple('='*42),
		C.red(len(sleigh.venues)),
		C.red(sleigh.numOfPapers())))
