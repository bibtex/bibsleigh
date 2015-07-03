#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for exporting LRJ definitions of bundles to the HTML frontpages

import Fancy, AST, Templates, sys, os, json, glob
sys.path.append(os.getcwd()+'/../beauty')
from NLP import superbaretext, baretext, trash
from LP import listify

ienputdir = '../json'
outputdir = '../frontend'
sleigh = AST.Sleigh(ienputdir + '/corpus')
C = Fancy.colours()

def matchfromsleigh(sleigh, pattern):
	path = pattern.split('/')
	# NB: could have been a simple bruteforce search with a getPureName check,
	# but that is too slow; this way the code is somewhat uglier but we skip
	# over entire venues and years that are of no interest to us
	for v in sleigh.venues:
		if v.getPureName() != path[0]:
			continue
		# print('Venue match on ', v.getPureName())
		for y in v.years:
			if y.year != path[1]:
				continue
			# print('\tYear match on ', y.getPureName())
			for c in y.confs:
				if c.getPureName() != '/'.join(path[:3]):
					continue
				# print('\t\tConf match on ', c.getPureName())
				# TODO or NOTTODO: implement other ways of matching
				if path[3] == '*':
					return c.papers
	return []

if __name__ == "__main__":
	print('{}: {} venues, {} papers\n{}'.format(\
		C.purple('BibSLEIGH'),
		C.red(len(sleigh.venues)),
		C.red(sleigh.numOfPapers()),
		C.purple('='*42)))
	for b in glob.glob(ienputdir + '/bundles/*.json'):
		purename = b.split('/')[-1][:-5]
		bun = json.load(open(b, 'r'))
		dl = '{}'.format(bun)
		uberlist = ''
		pcx = scx = 0
		for ven in bun['contents']:
			vname = list(ven.keys())[0]
			vconfs = ven[vname]
			vlst = '<dl><dt>{}</dt><dd>'.format(vname)
			clsts = []
			for con in ven[vname]:
				cname = list(con.keys())[0]
				cpapers = con[cname]
				clst = '<dl><dt>{}</dt><dd><dl class="toc">'.format(cname)
				plst = sorted(matchfromsleigh(sleigh, cpapers), key=AST.sortbypages)
				pcx += len(plst)
				clst += '\n'.join([p.getItem() for p in plst])
				clst += '</dl></dd></dl>'
				clsts.append(clst)
				scx += 1
			vlst += '\n'.join(clsts)
			vlst += '</dd></dl>'
			uberlist += vlst
		uberlist = '<h2>{} papers from {} sources</h2>{}'.format(pcx, scx, uberlist)
		f = open(outputdir + '/bundle/' + purename + '.html', 'w')
		f.write(Templates.bunHTML.format(
			title=purename+' bundle',
			bundle=bun['name'],
			ebundle=AST.escape(purename),
			dl=uberlist))
		f.close()
	print('{}\nDone with {} venues, {} papers, {} tags.'.format(\
		C.purple('='*42),
		C.red(len(sleigh.venues)),
		C.red(sleigh.numOfPapers()),
		C.red(sleigh.numOfTags())))
