#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for exporting stems/words to the HTML frontpages

import os.path
from fancy.ANSI import C
from fancy.Templates import wordlistHTML, wordHTML
from lib.AST import Sleigh, escape
from lib.JSON import parseJSON
from lib.NLP import ifApproved

ienputdir = '../json'
outputdir = '../frontend'
n2f_name = '_name2file.json'
name2file = parseJSON(n2f_name) if os.path.exists(n2f_name) else {}
sleigh = Sleigh(ienputdir + '/corpus', name2file)

def top5(d):
	ks = list(d.keys())
	byd = lambda z: -d[z]
	tops = sorted(ks[:5], key=byd)
	if len(ks) > 5:
		for kk in ks[5:]:
			if d[kk] > d[tops[-1]]:
				tops[-1] = kk
				if d[kk] > d[tops[-2]]:
					tops.sort(key=byd)
	return tops

if __name__ == "__main__":
	print('{}: {} venues, {} papers\n{}'.format(\
		C.purple('BibSLEIGH'),
		C.red(len(sleigh.venues)),
		C.red(sleigh.numOfPapers()),
		C.purple('='*42)))
	stems = sleigh.getStems()
	tagged = []
	for k in stems.keys():
		f = open('{}/word/{}.html'.format(outputdir, k), 'w')
		# papers are displayed in reverse chronological order
		lst = [x.getIItem() for x in \
			sorted(stems[k], key=lambda z: -z.json['year'] if 'year' in z.json.keys() else 0)]
		# collect other stems
		# NB: do not use the following code, slows everything down from 1 minute to 161 minutes
		# allstems = []
		# for x in stems[k]:
		# 	allstems += x.getBareStems()
		# siblings = {stem:allstems.count(stem) for stem in allstems if stem != k and ifApproved(stem)}
		# NB: the following code is faster:
		siblings = {}
		for x in stems[k]:
			for s in x.getBareStems():
				if s != k and ifApproved(s):
					siblings.setdefault(s, 0)
					siblings[s] += 1
		box = '<code>Used together with:</code><hr/>' + \
			'\n<br/>'.join(['<span class="tag"><a href="{0}.html">{0}</a></span> ({1})'.format(\
				S, siblings[S]) for S in top5(siblings)])
		f.write(wordHTML.format(\
			stem=k,
			inthebox=box,
			listname='{} papers'.format(len(lst)),
			dl='<dl class="toc">' + '\n'.join(lst).replace('href="', 'href="../') + '</dl>'))
		f.close()
	print('Word pages:', C.yellow('{}'.format(len(stems))), C.blue('generated'))
	# stem index
	f = open(outputdir+'/words.html', 'w')
	# TODO: add length mod
	keyz = [k for k in stems.keys() if ifApproved(k)]
	keyz.sort(key=lambda t: -len(t), reverse=True)
	lst = ['<li><a href="word/{}.html">{}</a>$ ({})</li>'.format(\
		escape(t), t, len(stems[t])) for t in keyz]
	ul = '<ul class="tri">' + '\n'.join(lst) + '</ul>'
	CX = sum([len(stems[t]) for t in stems.keys()])
	f.write(wordlistHTML.format(\
		title='All known stems',
		listname='{} stems known from {} notable words'.format(len(stems), CX),
		ul=ul))
	f.close()
	print('Stem index:', C.blue('created'))
	print('{}\nDone with {} venues, {} papers, {} tags.'.format(\
		C.purple('='*42),
		C.red(len(sleigh.venues)),
		C.red(sleigh.numOfPapers()),
		C.red(sleigh.numOfTags())))
