#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for exporting LRJs to the HTML frontpages

import Fancy, AST, Templates, sys, os, glob, json
sys.path.append(os.getcwd()+'/../beauty')
from NLP import superbaretext, baretext, trash
from JSON import parseJSON
from LP import listify

ienputdir = '../json'
outputdir = '../frontend'
sleigh = AST.Sleigh(ienputdir + '/corpus')
C = Fancy.colours()

def makeimg(fn, alt, w=''):
	if w:
		return '<img src="../stuff/{}.png" alt="{}" width="{}px"/>'.format(fn, alt, w)
	else:
		return '<img src="../stuff/{}.png" alt="{}"/>'.format(fn, alt)

def dict2links(d):
	rs = []
	for k in sorted(d.keys()):
		if k.isupper() or k == 'name':
			continue
		v = d[k]
		if k == 'g':
			rs.append(\
				(makeimg('ico-g', 'Google'),
				'<a href="https://www.google.com/search?q={}">{}</a>'.format(AST.escape(v), v)))
		elif k.endswith('.wp'):
			lang = k.split('.')[0]
			# TODO: make a dictionary of language names
			ico = makeimg('ico-wp', 'Wikipedia') + makeimg('ico-'+lang, 'Language')
			lang = k.split('.')[0]
			r = '<a href="https://{}.wikipedia.org/wiki/{}">{}</a>'.format(\
				lang, \
				AST.escape(v).replace('%20', '_'), \
				v)
			rs.append((ico,r))
		elif k == 'wd':
			rs.append(\
				(makeimg('ico-wd', 'Wikidata'),
				'<a href="https://www.wikidata.org/wiki/{0}">{0}</a>'.format(v)))
		elif k == 'dblp':
			# http://dblp.uni-trier.de/pers/hd/m/Major:Elaine
			rs.append(\
				(makeimg('ico-dblp', 'DBLP'),
				'<a href="http://dblp.uni-trier.de/pers/hd/{}/{}">DBLP: {}</a>'.format(\
				v[0].lower(),
				AST.escape(v),
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
					# r = '<img src="../stuff/{l}.png" alt="{u}" width="30px"> '.format(l=role[0].lower(), u=role[0])
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
	return '\n'.join(['<h3>{} {}</h3>'.format(r[0],r[1]) for r in rs])

def myparsejson(fn):
	j = json.load(open(fn, 'r'))
	j['FILE'] = fn
	return j

if __name__ == "__main__":
	print('{}: {} venues, {} papers\n{}'.format(\
		C.purple('BibSLEIGH'),
		C.red(len(sleigh.venues)),
		C.red(sleigh.numOfPapers()),
		C.purple('='*42)))
	ps = []
	# ts = sleigh.getTags()

	# tagged = []
	# for k in ts.keys():
	for fn in glob.glob(ienputdir + '/people/*.json'):
		k = fn.split('/')[-1][:-5]
		ps.append(k)
		f = open('{}/person/{}.html'.format(outputdir, k), 'w')
		# lst = [x.getRestrictedItem(k) for x in ts[k]]
		# no comprehension possible for this case
		# for x in ts[k]:
		# 	if x not in tagged:
		# 		tagged.append(x)
		# read tag definition
		persondef = myparsejson(fn)
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
		dl = ''
		# for k in persondef.keys():
		# 	if persondef[k].startswith('http'):
		# 		links += '<h2>{0}: <a href="{1}">{1}</a></h2>'.format(k, persondef[k])
		# 	else:
		# 		links += '<h2>{0}: {1}</h2>'.format(k, persondef[k])
		gender = ''
		if 'sex' in persondef.keys():
			if persondef['sex'] == 'Male':
				gender = '♂'
				del persondef['sex']
			elif persondef['sex'] == 'Female':
				gender = '♀'
				del persondef['sex']
		# links.extend([kv2link(jk, persondef[jk]) for jk in persondef.keys()\
		# 		if not jk.isupper() and jk != 'name'])
		# links = '\n'.join(links)
		links = dict2links(persondef)

		f.write(Templates.personHTML.format(
			title=k,
			gender=gender,
			eperson=AST.escape(k),
			person=k.replace('_', ' '),
			# boxlinks=links
			above=links,
			listname='{} papers'.format(0),#len(lst)),
			dl=dl))
		f.close()
	print('Person pages:', C.yellow('{}'.format(len(ps))), C.blue('generated'))
	# tag index
	f = open(outputdir+'/person/index.html', 'w')
	# keyz = [k for k in ps.keys() if len(ts[k]) > 2]
	# keyz = sorted(keyz, key=lambda t:len(ts[t]), reverse=True)
	keyz = ps#sorted(ps.keys())
	lst = ['<li><a href="{}.html">{}</a></li>'.format(AST.escape(t), t) for t in keyz]
	ul = '<ul class="mul">' + '\n'.join(lst) + '</ul>'
	# CX = sum([len(ts[t]) for t in ts.keys()])
	f.write(Templates.peoplistHTML.format(
		title='All contributors',
		listname='{} people known'.format(len(ps)),
		ul=ul))
	f.close()
	print('People index:', C.blue('created'))
	print('{}\nDone with {} venues, {} papers, {} tags.'.format(\
		C.purple('='*42),
		C.red(len(sleigh.venues)),
		C.red(sleigh.numOfPapers()),
		C.red(sleigh.numOfTags())))
	# print(sleigh.getTags())
