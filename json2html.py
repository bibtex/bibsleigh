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
	ts = sleigh.getTags()
	for k in ts.keys():
		f = open('{}/tag/{}.html'.format(outputdir, k), 'w')
		# lst = ['<dt><a href="../{}">'.format(x.getHtmlName()) for x in ts[k]]
		lst = [x.getItem() for x in ts[k]]
		# TODO: sort by venues!
		dl = '<dl><dt>All venues</dt><dd><dl class="toc">' + '\n'.join(sorted(lst)) + '</dl></dd></dl>'
		# hack to get from tags to papers
		dl = dl.replace('href="', 'href="../')
		f.write(Templates.tagHTML.format(
			title=k+' tag',
			tag=k,
			idx='',
			listname='{} papers'.format(len(lst)),
			dl=dl))
		f.close()
	f = open(outputdir+'/tag/index.html', 'w')
	lst = ['<li><a href="{0}.html">{0}</a> ({1})</li>'.format(t, len(ts[t])) for t in ts.keys()]
	ul = '<ul class="tag">' + '\n'.join(sorted(lst)) + '</ul>'
	f.write(Templates.tagHTML.format(
		title='All known tags',
		tag='',
		idx=' index',
		listname='{} tags known'.format(len(ts.keys())),
		dl=ul))
	f.close()
	print('{}\nDone with {} venues, {} papers, {} tags.'.format(\
		C.purple('='*42),
		C.red(len(sleigh.venues)),
		C.red(sleigh.numOfPapers()),
		C.red(sleigh.numOfTags())))
	# print(sleigh.getTags())
