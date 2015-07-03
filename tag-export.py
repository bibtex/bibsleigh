#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for exporting LRJs to the HTML frontpages

import Fancy, AST, Templates, sys, os
sys.path.append(os.getcwd()+'/../beauty')
from NLP import superbaretext, baretext, trash
from JSON import parseJSON
from LP import listify

ienputdir = '../json'
outputdir = '../frontend'
sleigh = AST.Sleigh(ienputdir + '/corpus')
C = Fancy.colours()

def makeimg(fn, alt):
	return '<img src="../stuff/ico-{}.png" alt="{}"/>'.format(fn, alt)

def kv2link(k, v):
	if k == 'g':
		ico = makeimg('g', 'Google')
		r = '<a href="https://www.google.com/search?q={0}">{0}</a>'.format(v)
	elif k.endswith('.wp'):
		lang = k.split('.')[0]
		# TODO: make a dictionary of language names
		ico = makeimg('wp', 'Wikipedia') + makeimg(lang, 'Language')
		lang = k.split('.')[0]
		r = '<a href="https://{0}.wikipedia.org/wiki/{1}">{1}</a>'.format(lang, v)
	elif k == 'wd':
		ico = makeimg('wd', 'Wikidata')
		r = '<a href="https://www.wikidata.org/wiki/{0}">{0}</a>'.format(v)
	elif k == 'hwiki':
		ico = makeimg('h', 'Haskell Wiki')
		r = '<a href="https://wiki.haskell.org/{0}">{0}</a>'.format(v)
	elif k == 'so':
		ico = makeimg('so', 'Stack Overflow')
		r = '<a href="http://stackoverflow.com/questions/tagged?tagnames={0}">{0}</a>'.format(v)
	elif k == 'www':
		ico = ''#makeimg('www', 'Homepage')
		if not v.startswith('http'):
			w = v
			v = 'http://'+v
		else:
			w = v.replace('http://', '').replace('https://', '')
		r = '<a href="{0}">{1}</a>'.format(v, w)
	elif k == 'aka':
		ico = ''
		r = '<br/>'.join(['a.k.a.: “{}”'.format(x) for x in listify(v)])
	else:
		ico = ''
		r = '?{}?{}?'.format(k, v)
	return ico + ' ' + r + '<br/>'

if __name__ == "__main__":
	print('{}: {} venues, {} papers\n{}'.format(\
		C.purple('BibSLEIGH'),
		C.red(len(sleigh.venues)),
		C.red(sleigh.numOfPapers()),
		C.purple('='*42)))
	ts = sleigh.getTags()
	tagged = []
	for k in ts.keys():
		f = open('{}/tag/{}.html'.format(outputdir, k), 'w')
		lst = [x.getRestrictedItem(k) for x in ts[k]]
		# no comprehension possible for this case
		for x in ts[k]:
			if x not in tagged:
				tagged.append(x)
		# read tag definition
		tagdef = parseJSON(ienputdir + '/tags/{}.json'.format(k))
		# what to google?
		links = []
		if 'g' not in tagdef.keys():
			links.append(kv2link('g', tagdef['namefull'] if 'namefull' in tagdef.keys() else k))
		links.extend([kv2link(jk, tagdef[jk]) for jk in tagdef.keys()\
				if not jk.isupper()
				and not jk.startswith('match')
				and not jk.startswith('name')
				and jk != 'relieves'])
		title = tagdef['namefull'] if 'namefull' in tagdef.keys() else tagdef['name']
		subt = ('<br/><em>'+tagdef['namelong']+'</em>') if 'namelong' in tagdef.keys() else ''
		links = '<strong>{}</strong>{}<hr/>'.format(title, subt) + '\n'.join(sorted(links))
		# TODO: sort by venues!
		dl = '<dl><dt>All venues</dt><dd><dl class="toc">' + '\n'.join(sorted(lst)) + '</dl></dd></dl>'
		# hack to get from tags to papers
		dl = dl.replace('href="', 'href="../')
		f.write(Templates.tagHTML.format(
			title=k+' tag',
			tag=k,
			above='',
			boxlinks=links,
			listname='{} papers'.format(len(lst)),
			dl=dl))
		f.close()
	print('Tag pages:', C.blue('generated'))
	# tag index
	f = open(outputdir+'/tag/index.html', 'w')
	keyz = [k for k in ts.keys() if len(ts[k]) > 2]
	keyz = sorted(keyz, key=lambda t:len(ts[t]), reverse=True)
	lst = ['<li><a href="{}.html">{}</a> ({})</li>'.format(AST.escape(t), t, len(ts[t])) for t in keyz]
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
		boxlinks='',
		listname='{} papers still untagged'.format(CX),
		dl=dl.replace('href="', 'href="../')))
	f.close()
	print('{}\nDone with {} venues, {} papers, {} tags.'.format(\
		C.purple('='*42),
		C.red(len(sleigh.venues)),
		C.red(sleigh.numOfPapers()),
		C.red(sleigh.numOfTags())))
	# print(sleigh.getTags())
