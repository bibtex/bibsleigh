#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import Fancy, AST, Templates

ienputdir = '../json'
outputdir = '../frontend'
sleigh = AST.Sleigh(ienputdir)
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
	# now for tags
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
			listname='{} papers'.format(len(lst)),
			dl=dl))
		f.close()
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
	# untagged papers
	f = open(outputdir+'/tag/untagged.html', 'w')
	dl = '<dl class="toc">'
	CX = 0
	for v in sleigh.venues:
		for c in v.getConfs():
			for p in c.papers:
				if p in tagged:
					continue
				dl += '\n' + p.getItem()
				CX += 1
	dl += '</dl>'
	f.write(Templates.tagHTML.format(
		title='All untagged papers',
		tag='untagged',
		listname='{} papers still untagged'.format(CX),
		dl=dl.replace('href="', 'href="../')))
	f.close()
	print('{}\nDone with {} venues, {} papers, {} tags.'.format(\
		C.purple('='*42),
		C.red(len(sleigh.venues)),
		C.red(sleigh.numOfPapers()),
		C.red(sleigh.numOfTags())))
	# print(sleigh.getTags())
