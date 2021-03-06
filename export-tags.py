#!/c/Users/vadim/AppData/Local/Programs/Python/Python37-32/python
# -*- coding: utf-8 -*-
#
# a module for exporting LRJ definitions of tags to the HTML frontpages

import os.path
from fancy.ANSI import C
from fancy.Languages import ISONames
from fancy.Templates import taglistHTML, tagHTML
from lib.AST import Sleigh, escape
from lib.JSON import parseJSON
from lib.LP import listify
from lib.NLP import string2words, trash

ienputdir = '../json'
outputdir = '../frontend'
n2f_name = '_name2file.json'
name2file = parseJSON(n2f_name) if os.path.exists(n2f_name) else {}
sleigh = Sleigh(ienputdir + '/corpus', name2file)

def makeimg(fn, alt):
	return '<img src="../stuff/ico-{}.png" alt="{}"/>'.format(fn, alt)

def kv2link(k, v):
	if k == 'g':
		ico = makeimg('g', 'Google')
		r = '<a href="https://www.google.com/search?q={}">{}</a>'.format(escape(v), v)
	elif k.endswith('.wp'):
		lang = k.split('.')[0]
		# Using ISO 639-1 language names
		ico = makeimg('wp', 'Wikipedia') + makeimg(lang, ISONames[lang])
		lang = k.split('.')[0]
		r = '<a href="https://{}.wikipedia.org/wiki/{}">{}</a>'.format(\
			lang, \
			escape(v).replace('%20', '_'), \
			v)
	elif k.endswith('.wb'):
		lang = k.split('.')[0]
		# Using ISO 639-1 language names
		ico = makeimg('wb', 'Wikibooks') + makeimg(lang, ISONames[lang])
		lang = k.split('.')[0]
		r = '<a href="https://{}.wikibooks.org/wiki/{}">{}</a>'.format(\
			lang, \
			escape(v).replace('%20', '_'), \
			v)
	elif k == 'wd':
		ico = makeimg('wd', 'Wikidata')
		r = '<a href="https://www.wikidata.org/wiki/{0}">{0}</a>'.format(v)
	elif k == 'hwiki':
		ico = makeimg('h', 'Haskell Wiki')
		r = '<a href="https://wiki.haskell.org/{}">{}</a>'.format(escape(v), v)
	elif k == 'so':
		ico = makeimg('so', 'Stack Overflow')
		r = '<a href="http://stackoverflow.com/questions/tagged?tagnames={0}">{0}</a>'.format(v)
	elif k == 'www':
		ico = ''#makeimg('www', 'Homepage')
		if not v.startswith('http'):
			y = v
			v = 'http://'+v
		else:
			y = v.replace('http://', '').replace('https://', '')
		r = '<a href="{0}">{1}</a>'.format(v, y)
	elif k == 'aka':
		ico = ''
		r = '<br/>'.join(['a.k.a.: “{}”'.format(z) for z in listify(v)])
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
	for key in ts.keys():
		f = open('{}/tag/{}.html'.format(outputdir, key), 'w', encoding='utf-8')
		# papers are displayed in reverse chronological order
		lst = [x.getRestrictedItem(key) for x in \
			sorted(ts[key], key=lambda z: -z.json['year'] if 'year' in z.json.keys() else 0)]
		# no comprehension possible for this case
		for x in ts[key]:
			if x not in tagged:
				tagged.append(x)
		# read tag definition
		p = ienputdir + '/tags/{}.json'.format(key)
		if not os.path.exists(p):
			print(C.red('Error') + ' opening ' + p)
			continue
		tagdef = parseJSON(p)
		# what to google?
		links = []
		if 'g' not in tagdef.keys():
			links.append(kv2link('g', tagdef['namefull'] if 'namefull' in tagdef.keys() else key))
		links.extend([kv2link(jk, tagdef[jk]) for jk in tagdef.keys()\
				if not jk.isupper() \
				and not jk.startswith('match') \
				and not jk.startswith('name') \
				and jk != 'relieves'])
		title = tagdef['namefull'] if 'namefull' in tagdef.keys() else tagdef['name']
		subt = ('<br/><em>'+tagdef['namelong']+'</em>') if 'namelong' in tagdef.keys() else ''
		links = '<strong>{}</strong>{}<hr/>'.format(title, subt) + '\n'.join(sorted(links))
		dl = '<dl class="toc">' + '\n'.join(lst) + '</dl>'
		# hack to get from tags to papers
		dl = dl.replace('href="', 'href="../')
		f.write(tagHTML.format(\
			title=key+' tag',
			etag=escape(key),
			tag=key,
			above='',
			boxlinks=links,
			listname='{} papers'.format(len(lst)),
			dl=dl))
		f.close()
	print('Tag pages:', C.yellow('{}'.format(len(ts))), C.blue('generated'))
	# tag index
	f = open(outputdir+'/tag/index.html', 'w', encoding='utf-8')
	keyz = [q for q in ts.keys() if len(ts[q]) > 2]
	keyz.sort(key=lambda t: len(ts[t]), reverse=True)
	lst = ['<li>#<a href="{}.html">{}</a> ({})</li>'.format(escape(t), t, len(ts[t])) for t in keyz]
	ul = '<ul class="tri mul">' + '\n'.join(lst) + '</ul>'
	CX = sum([len(ts[t]) for t in ts.keys()])
	f.write(taglistHTML.format(\
		title='All known tags',
		listname='{} tags known from {} markings'.format(len(ts), CX),
		ul=ul))
	f.close()
	print('Tag index:', C.blue('created'))
	# untagged papers
	f = open(outputdir+'/tag/untagged.html', 'w', encoding='utf-8')
	CX = 0
	# bag of words
	bow = {}
	lst = []
	for V in sleigh.venues:
		for c in V.getConfs():
			for p in c.papers:
				if p in tagged:
					continue
				lst.append(p)
				CX += 1
				for w in string2words(p.get('title')):
					if len(w) < 3 or w in trash:
						continue
					if w in bow.keys():
						bow[w] += 1
					else:
						bow[w] = 1
	print('Tag candidates:', C.blue('found'))
	bag = '\n'
	bowkeys = sorted(bow.keys(), key=lambda z: -int(bow[z]))
	for w in bowkeys:
		bag += '<span style="border:1px solid black;margin:5px">{}</span> ({}) '.format(w, bow[w])
		if bow[w] < 30:
			break
	lst = [x.getRestrictedItem(None) for x in \
		sorted(lst, key=lambda z: -z.json['year'] if 'year' in z.json.keys() else 0)]
	dl = '<dl class="toc">' + '\n'.join(lst) + '</dl>'
	f.write(tagHTML.format(\
		title='All untagged papers',
		tag='untagged',
		etag='untagged', # TODO: figure out a way to remove the edit link from here
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
