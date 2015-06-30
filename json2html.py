#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for exporting LRJs to the HTML frontpages

import Fancy, AST, Templates, sys, os
sys.path.append(os.getcwd()+'/../beauty')
from NLP import superbaretext, baretext

ienputdir = '../json'
outputdir = '../frontend'
sleigh = AST.Sleigh(ienputdir)
C = Fancy.colours()
trash = ('on', 'an', 'for', 'of', 'a', 'the', '-', 'to', 'from', 'by', 'in', 'with', 's', 'as', 'at', 'via', 'how', 'towards')

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
	# now for tags
	print(C.purple('='*42))
	ts = sleigh.getTags()
	tagged = []
	for k in ts.keys():
		f = open('{}/tag/{}.html'.format(outputdir, k), 'w')
		lst = [x.getItem() for x in ts[k]]
		# no comprehension possible for this case
		for x in ts[k]:
			if x not in tagged:
				tagged.append(x)
		# TODO: sort by venues!
		dl = '<dl><dt>All venues</dt><dd><dl class="toc">' + '\n'.join(sorted(lst)) + '</dl></dd></dl>'
		# hack to get from tags to papers
		dl = dl.replace('href="', 'href="../')
		f.write(Templates.tagHTML.format(
			title=k+' tag',
			tag=k,
			above='',
			listname='{} papers'.format(len(lst)),
			dl=dl))
		f.close()
	print('Tag pages:', C.blue('generated'))
	# tag index
	f = open(outputdir+'/tag/index.html', 'w')
	keyz = [k for k in ts.keys() if len(ts[k]) > 2]
	keyz = sorted(keyz, key=lambda t:len(ts[t]), reverse=True)
	lst = ['<li><a href="{0}.html">{0}</a> ({1})</li>'.format(t, len(ts[t])) for t in keyz]
	ul = '<ul class="tag mul">' + '\n'.join(lst) + '</ul>'
	CX = sum([len(ts[t]) for t in ts.keys()])
	f.write(Templates.taglistHTML.format(
		title='All known tags',
		tag='',
		listname='{} tags known from {} markings'.format(len(ts.keys()), CX),
		dl=ul))
	f.close()
	print('Tag index:', C.blue('created'))
	# untagged papers
	f = open(outputdir+'/tag/untagged.html', 'w')
	dl = '<dl class="toc">'
	CX = 0
	# bag of words
	bow = {}
	for v in sleigh.venues:
		for c in v.getConfs():
			for p in c.papers:
				if p in tagged:
					continue
				dl += '\n' + p.getItem()
				CX += 1
				for w in superbaretext(baretext(p.get('title'))).split(' '):
					if w in trash:
						continue
					if w in bow.keys():
						bow[w] += 1
					else:
						bow[w] = 1
	print('Tag candidates:', C.blue('found'))
	bag='\n'
	for w in bow.keys():
		if bow[w] > 40:
			bag += '<span style="border:1px solid black;margin:5px">'+w+'</span> '
	dl += '</dl>'
	f.write(Templates.tagHTML.format(
		title='All untagged papers',
		tag='untagged',
		above=bag,
		listname='{} papers still untagged'.format(CX),
		dl=dl.replace('href="', 'href="../')))
	f.close()
	print('{}\nDone with {} venues, {} papers, {} tags.'.format(\
		C.purple('='*42),
		C.red(len(sleigh.venues)),
		C.red(sleigh.numOfPapers()),
		C.red(sleigh.numOfTags())))
	# print(sleigh.getTags())
