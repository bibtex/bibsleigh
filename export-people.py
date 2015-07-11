#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for exporting LRJs to the HTML frontpages

import os.path, json, glob
from fancy.ANSI import C
from fancy.Languages import ISONames
from fancy.Templates import personHTML, peoplistHTML, movein
from lib.AST import Sleigh, escape
from lib.JSON import parseJSON

# The idea is to generate a colour between FFFDE7 (for 'a') and F57F17 (for 'z')
# FFFDE7 is Yellow/50 and F57F17 is Yellow/900 in Material Design
def genColour(az):
	# get something between 0 and 25
	i = ord(az) - ord('a')
	r = 0xFF - (0xFF - 0xF5)*i//26
	g = 0xFD - (0xFD - 0x7F)*i//26
	b = 0xE7 - (0xE7 - 0x17)*i//26
	return hex(r)[-2:] + hex(g)[-2:] + hex(b)[-2:]

ienputdir = '../json'
outputdir = '../frontend'
sleigh = Sleigh(ienputdir + '/corpus')

def makeimg(ifn, alt, w=''):
	if w:
		return '<img src="../stuff/{}.png" alt="{}" width="{}px"/>'.format(ifn, alt, w)
	else:
		return '<img src="../stuff/{}.png" alt="{}"/>'.format(ifn, alt)

def dict2links(d):
	rs = []
	for k in sorted(d.keys()):
		if k.isupper() or k in ('name', 'authored', 'roles'):
			continue
		v = d[k]
		if k == 'g':
			rs.append(\
				(makeimg('ico-g', 'Google'),\
				'<a href="https://www.google.com/search?q={}">{}</a>'.format(escape(v), v)))
		elif k.endswith('.wp'):
			lang = k.split('.')[0]
			# Using ISO 639-1 language names
			ico = makeimg('ico-wp', 'Wikipedia') + makeimg('ico-'+lang, ISONames[lang])
			lang = k.split('.')[0]
			r = '<a href="https://{}.wikipedia.org/wiki/{}">{}</a>'.format(\
				lang, \
				escape(v).replace('%20', '_'), \
				v)
			rs.append((ico, r))
		elif k == 'wd':
			rs.append(\
				(makeimg('ico-wd', 'Wikidata'),\
				'<a href="https://www.wikidata.org/wiki/{0}">{0}</a>'.format(v)))
		elif k == 'dblp':
			# http://dblp.uni-trier.de/pers/hd/m/Major:Elaine
			rs.append(\
				(makeimg('ico-dblp', 'DBLP'),\
				'<a href="http://dblp.uni-trier.de/pers/hd/{}/{}">DBLP: {}</a>'.format(\
				v[0].lower(),
				escape(v),
				v)))
		elif k == 'www':
			if not v.startswith('http'):
				w = v
				v = 'http://'+v
			else:
				w = v.replace('http://', '').replace('https://', '')
			rs.append(('', '<a href="{0}">{1}</a>'.format(v, w)))
		elif k == 'sex':
			ico = ''
			rs.append(('', 'Gender: ' + v))
		elif k == 'roles':
			for role in v:
				if os.path.exists(outputdir + '/stuff/' + role[0].lower() + '.png'):
					ico = makeimg(role[0].lower(), role[0], 30)
				else:
					ico = ''
				if os.path.exists(outputdir + '/' + role[0] + '-' + role[1] + '.html'):
					r = '<a href="../{0}-{1}.html">{0}-{1}</a>'.format(role[0], role[1])
				else:
					r = '{0}-{1}'.format(role[0], role[1])
				rs.append((ico, r + ' ' + role[2]))
		else:
			rs.append(('', '{}: {}'.format(k, v)))
	# print(rs)
	return '\n'.join(['<h3>{} {}</h3>'.format(r[0], r[1]) for r in rs])

def countAllPapers(ad, ed):
	if ad == 0 and ed == 0:
		return 'No papers'
	if ad == 0 and ed != 0:
		return 'Edited {} volumes edited'.format(ed)
	if ad != 0 and ed == 0:
		return 'Authored {} papers'.format(ad)
	if ad != 0 and ed == 0:
		return 'Authored {} papers'.format(ad)

if __name__ == "__main__":
	print('{}: {} venues, {} papers\n{}'.format(\
		C.purple('BibSLEIGH'),
		C.red(len(sleigh.venues)),
		C.red(sleigh.numOfPapers()),
		C.purple('='*42)))
	ps = []
	# flatten the sleigh
	bykey = {}
	for v in sleigh.venues:
		bykey[v.getKey()] = v
		for c in v.getConfs():
			bykey[c.getKey()] = c
			for p in c.papers:
				bykey[p.getKey()] = p
	print(C.purple('BibSLEIGH flattened to {} papers'.format(len(bykey))))
	# tagged = []
	# for k in ts.keys():
	for fn in glob.glob(ienputdir + '/people/*.json'):
		k = fn.split('/')[-1][:-5]
		ps.append(k)
		f = open('{}/person/{}.html'.format(outputdir, k), 'w')
		persondef = parseJSON(fn)
		# what to google?
		# links = []
		# if 'g' not in persondef.keys():
		# 	links.append(kv2link('g', tagdef['name'] if 'namefull' in tagdef.keys() else k))
		# title = tagdef['namefull'] if 'namefull' in tagdef.keys() else tagdef['name']
		# subt = ('<br/><em>'+tagdef['namelong']+'</em>') if 'namelong' in tagdef.keys() else ''
		# links = '<strong>{}</strong>{}<hr/>'.format(title, subt) + '\n'.join(sorted(links))
		# TODO: sort by venues!
		# dl = '<dl><dt>All venues</dt><dd><dl class="toc">' + '\n'.join(sorted(lst)) + '</dl></dd></dl>'
		# hack to get from tags to papers
		# dl = dl.replace('href="', 'href="../')
		gender = ''
		if 'sex' in persondef.keys():
			if persondef['sex'] == 'Male':
				gender = '♂'
				del persondef['sex']
			elif persondef['sex'] == 'Female':
				gender = '♀'
				del persondef['sex']
		dls = dict2links(persondef)
		if 'roles' in persondef.keys():
			curlist = '<h3>Facilitated {} volumes:</h3>'.format(len(persondef['roles']))
			# things = [sleigh.seekByKey(p).getItem() for p in persondef['edited']]
			things = [bykey[r[0]].getIconItem(r[1]) for r in persondef['roles']]
			# curlist += '<dl class="toc">' + movein('\n'.join(things)) + '</dl>'
			curlist += '<div class="minibar">' + movein('\n'.join(things)) + '<br style="clear:both"/></div>'
			dls += curlist
		if 'authored' in persondef.keys():
			curlist = '<h3>Wrote {} papers:</h3>'.format(len(persondef['authored']))
			# things = [sleigh.seekByKey(p).getItem() for p in persondef['authored']]
			things = [bykey[p].getItem() for p in persondef['authored']]
			curlist += '<dl class="toc">' + movein('\n'.join(things)) + '</dl>'
			dls += curlist
		f.write(personHTML.format(\
			title=k,
			gender=gender,
			eperson=escape(k),
			person=persondef['name'],#k.replace('_', ' '),
			# boxlinks=links
			namedlists=dls))
		f.close()
	print('Person pages:', C.yellow('{}'.format(len(ps))), C.blue('generated'))
	# person index
	# keyz = [k for k in ps.keys() if len(ts[k]) > 2]
	# keyz = sorted(keyz, key=lambda t:len(ts[t]), reverse=True)
	keyz = ps#sorted(ps.keys())
	letters = [chr(x) for x in range(ord('a'), ord('z')+1)]
	indices = {x:[] for x in letters}
	for t in keyz:
		letter = t.split('_')[-1][0].lower()
		if not letter.isalpha():
			print(C.red('ERROR')+':', 'wrong name', t)
			continue
		indices[letter].append('<li><a href="{}.html">{}</a></li>'.format(\
			escape(t),
			t.replace('_', ' ')))
	# fancy yellow A-Z link array
	links = \
	['<div class="abc" style="background:#{col}"><a href="index-{low}.html">{up}</a></div>'.format(\
		col=genColour(letter),
		low=letter,
		up=letter.upper()) for letter in letters]
	azlist = '\n'.join(links)+'<br style="clear:both"/>\n'
	# index-a, index-b, etc: one index for all is too big
	for letter in letters:
		f = open('{}/person/index-{}.html'.format(outputdir, letter), 'w')
		f.write(peoplistHTML.format(\
			title='All {}* contributors'.format(letter.upper()),
			listname='{} people known'.format(len(indices[letter])),
			ul=azlist+'<ul class="tri mul">' + '\n'.join(indices[letter]) + '</ul>'\
		))
		f.close()
	# the main index only contains links to A-Z indices
	f = open('{}/person/index.html'.format(outputdir), 'w')
	f.write(peoplistHTML.format(\
		title='All contributors',
		listname='{} people known'.format(len(ps)),
		ul=azlist
	))
	f.close()
	print('People index:', C.blue('created'))
	print('{}\nDone with {} venues, {} papers, {} tags.'.format(\
		C.purple('='*42),
		C.red(len(sleigh.venues)),
		C.red(sleigh.numOfPapers()),
		C.red(sleigh.numOfTags())))
	# print(sleigh.getTags())
