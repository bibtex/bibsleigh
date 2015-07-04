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
pcx = 0

def matchfromsleigh(sleigh, pattern):
	if isinstance(pattern, list):
		paths = []
		cur = '???'
		for p in pattern:
			if p.find('/') < 0:
				paths.append(cur + '/' + p)
			else:
				paths.append(p)
			cur = paths[-1][:paths[-1].rindex('/')]
		res = []
		for p in paths:
			res.extend(matchfromsleigh(sleigh, p))
		return res
	else:
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
				else:
					return [p for p in c.papers if p.getKey() in path[3]]
	return []

def processSortedRel(r):
	# [ {"x" : Y } ] where Y can be a string or a sorted rel
	global pcx
	acc = []
	for el in r:
		ename = list(el.keys())[0]
		evals = el[ename]
		if os.path.isfile(outputdir + '/stuff/' + ename.lower() + '.png'):
			img = '<img src="../stuff/{1}.png" alt="{0}" width="30px"/> '.format(ename, ename.lower())
		else:
			img = ''
		if isinstance(evals, str):
			plst = sorted(matchfromsleigh(sleigh, evals), key=AST.sortbypages)
			pcx += len(plst)
			ptxt = '<dl class="toc">'+'\n'.join([p.getItem() for p in plst])+'</dl>'
		elif isinstance(evals, list) and isinstance(evals[0], str):
			plst = sorted(matchfromsleigh(sleigh, evals), key=AST.sortbypages)
			pcx += len(plst)
			ptxt = '<dl class="toc">'+'\n'.join([p.getItem() for p in plst])+'</dl>'
		elif isinstance(evals, list) and isinstance(evals[0], dict):
			ptxt = processSortedRel(evals)
			clss = ''
		else:
			print(C.red('ERROR:'), 'unrecornised bundle structure', evals)
		acc.append('<dl><dt>{}{}</dt><dd>{}</dl>'.format(img, ename, ptxt))
	return '\n'.join(acc)

if __name__ == "__main__":
	print('{}: {} venues, {} papers\n{}'.format(\
		C.purple('BibSLEIGH'),
		C.red(len(sleigh.venues)),
		C.red(sleigh.numOfPapers()),
		C.purple('='*42)))
	bundles = {}
	for b in glob.glob(ienputdir + '/bundles/*.json'):
		purename = b.split('/')[-1][:-5]
		bun = json.load(open(b, 'r'))
		uberlist = '<h2>{1} papers</h2>{0}'.format(processSortedRel(bun['contents']), pcx)
		f = open(outputdir + '/bundle/' + purename + '.html', 'w')
		f.write(Templates.bunHTML.format(
			title=purename+' bundle',
			bundle=bun['name'],
			ebundle=AST.escape(purename),
			dl=uberlist.replace('href="', 'href="../').replace('../mailto', 'mailto')))
		f.close()
		bundles[purename] = pcx
	print('Bundle pages:', C.yellow('{}'.format(len(bundles))), C.blue('generated'))
	# now for the index
	f = open(outputdir+'/bundle/index.html', 'w')
	lst = ['<li><a href="{}.html">{}</a> ({})</li>'.format(AST.escape(b), b, bundles[b]) for b in sorted(bundles.keys())]
	ul = '<ul class="tri">' + '\n'.join(lst) + '</ul>'
	f.write(Templates.bunListHTML.format(
		title='All specified bundles',
		listname='{} bundles known with {} papers'.format(len(bundles), sum(bundles.values())),
		ul='<ul class="tri">' + '\n'.join(lst) + '</ul>'))
	f.close()
	print('Bundle index:', C.blue('created'))
	print('{}\nDone with {} venues, {} papers.'.format(\
		C.purple('='*42),
		C.red(len(sleigh.venues)),
		C.red(sleigh.numOfPapers())))
