#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import os.path, glob, sys
# from template import confHTML, uberHTML
from Templates import uberHTML
from AST import *

# import os, sys, glob
# from template import uberHTML, confHTML, bibHTML, hyper_series
# from supported import supported

inputdir  = '../bibtest'
outputdir = '../frontend3'

def last(xx):
	return xx.split('/')[-1].replace('.json', '')

def parent(xx):
	return xx[:xx.rfind('/')]
	# return xx.split('/')[-1].replace('.json', '')

if __name__ == "__main__":
	venues = []
	for d in glob.glob(inputdir+'/*'):
		venues.append(Venue(d))
	print('{} venues, {} papers'.format(len(venues), sum([v.numOfPapers() for v in venues])))
	f = open(outputdir+'/index.html', 'w')
	f.write(uberHTML.format('\n'.join([v.getItem() for v in venues])))
	f.close()
	for v in venues:
		f = open(outputdir+'/'+v.getKey()+'.html', 'w')
		f.write(v.getPage())
		f.close()
		for c in v.getConfs():
			print('Conf:', c.getKey())
			f = open(outputdir+'/'+c.getKey()+'.html', 'w')
			f.write(c.getPage())
			f.close()
	sys.exit(0)
	GCX = 0
	# allconfs = []
	bib = {}
	traverseDir(inputdir, '', bib)
	print('[Total: {} entries]'.format(len(bib)))
	print('-'*100)
	for k in bib.keys():
		j = bib[k]
		pr = 1 if parent(k) in bib.keys() else 0
		children = [kk for kk in bib.keys() if kk.startswith(k) and kk[len(k):] != '' and kk[len(k)+1:].find('/') < 0]
		types = [bib[x]['type'] for x in children if 'type' in bib[x].keys()]
		if len(children)>1:
			print('{}: {} parents, {} children'.format(k, pr, len(children)))
		editions = contents = bibfield = text = ''
		if 'proceedings' in types:
			byY = {}
			for x in children:
				if bib[x]['year'] not in byY.keys():
					byY[bib[x]['year']] = []
				byY[bib[x]['year']].append(x)
			ys = ''
			for y in reversed(sorted(byY.keys())):
				ys += '<dt>{}</dt>'.format(y)
				for p in byY[y]:
					if 'booktitle' in bib[p].keys():
						bt = bib[p]['booktitle']
					elif 'title' in bib[p].keys():
						bt = bib[p]['title']
					else:
						bt = '???'
					ys += '<dd><a href="{}.html">{}</a> ({} {})</dd>'.format(p, bt, bib[p]['venue'], bib[p]['year'])
			editions = '<h3>Editions:</h3><dl>{}</dl>'.format(ys)
		if 'article' in types or 'inproceedings' in types:
			contents = '...'
		if pr == 0:
			# TODO: save for index.html
			pass
		f = open(last(k).replace(inputdir, outputdir), 'w')
		html = text + bibfield + editions + contents
		if 'title' not in bib[k] or not isinstance(bib[k]['title'], str):
			print('ERROR:', bib[k])
			continue
		cname = '%s (%s)' % (bib[k]['title'], bib[k]['year'])
		f.write(confHTML.format(img=bib[k]['title'].lower(), title=bib[k]['title'], fname=cname, dl=html))
		f.close()
