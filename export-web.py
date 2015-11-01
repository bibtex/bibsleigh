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
corpusdir = ienputdir + '/corpus'
outputdir = '../frontend'
n2f_name = '_name2file.json'
name2file = parseJSON(n2f_name) if os.path.exists(n2f_name) else {}
sleigh = Sleigh(corpusdir, name2file)

def nextYear(vvv):
	return int(sorted(glob.glob(vvv+'/*'))[-2].split('/')[-1])+1

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
		r = C.blue(v.getKey())
		f = open(outputdir+'/'+v.getKey()+'.html', 'w')
		f.write(v.getPage())
		f.close()
		if v.brands:
			r += '{' + '+'.join([C.blue(b.getKey()) for b in v.brands]) + '}'
			for b in v.brands:
				f = open(outputdir+'/'+b.getKey()+'.brand.html', 'w')
				f.write(b.getPage())
				f.close()
		r += ' => '
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
	pngs = [png.split('/')[-1].split('.')[0] for png in glob.glob(outputdir + '/stuff/*.png')]
	pngs = [png for png in pngs \
		if not (png.startswith('a-') or png.startswith('p-') or png.startswith('ico-')\
		or png in ('cc-by', 'xhtml', 'css', 'open-knowledge', 'edit'))]
	for brand in glob.glob(outputdir + '/*.brand.html'):
		pure = brand.split('/')[-1].split('.')[0]
		img = pure.lower().replace(' ', '')
		if img in pngs:
			pic = '<div class="wider"><a href="{0}"><img class="abc" src="{1}" alt="{2}"/></a><span>{2}</span></div>'.format(\
				brand,
				'stuff/'+img+'.png',
				pure)
			pngs.remove(img)
			icons.append(pic)
		else:
			# print('No image for', pure)
			pass
	corner = {'ada': 'TRI-Ada', 'comparch': 'CompArch', 'floc': 'FLoC', 'bibsleigh': 'index'}
	for pure in pngs:
		venueCandidate = corner[pure] if pure in corner else pure.upper()
		canlink = sorted(glob.glob(outputdir + '/' + venueCandidate + '*.html'), key=len)
		if canlink:
			pic = '<div class="wider"><a href="{0}"><img class="abc" src="stuff/{1}.png" alt="{2}"/></a><span>{2}</span></div>'.format(\
				canlink[0],
				pure,
				venueCandidate,
				canlink[0].split('/')[0])
		elif pure == 'twitter':
			pic = '<div class="wider"><a href="https://about.twitter.com/company/brand-assets"><img class="abc" src="stuff/twitter.png" alt="Twitter"/></a><span>Twitter</span></div>'
		elif pure == 'email':
			pic = '<div class="wider"><a href="mailto:vadim@grammarware.net"><img class="abc" src="stuff/email.png" alt="e-mail"/></a><span>email</span></div>'
		else:
			print('Lonely', pure)
			pic = '<img class="abc" src="stuff/{0}.png" alt="{0}"/>'.format(pure)
		icons.append(pic)
	# find last year of each venue
	newstuff = ''
	# for ven in glob.glob(corpusdir + '/*'):
	# 	venname = ven.split('/')[-1]
	# 	newstuff += '<strong><a href="http://dblp.uni-trier.de/db/conf/{}/">{} {}</a></strong>, '.format(venname.lower(), venname, nextYear(ven))
		# print(ven.split('/')[-1], ':', lastYear(ven))
	# write "more info" file
	f = open(outputdir+'/about.html', 'w')
	f.write(aboutHTML.format(\
		len(icons),
		'<div class="minibar">' + '\n'.join(sorted(icons)) + '</div>',
		newstuff\
		))
	f.close()
	print('{}\nDone with {} venues, {} papers.'.format(\
		C.purple('='*42),
		C.red(len(sleigh.venues)),
		C.red(sleigh.numOfPapers())))
