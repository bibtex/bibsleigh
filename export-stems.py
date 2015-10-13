#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for exporting stems/words to the HTML frontpages

import os.path
from fancy.ANSI import C
from fancy.Templates import wordlistHTML, wordHTML
from lib.AST import Sleigh, escape
from lib.JSON import parseJSON
from lib.NLP import trash

ienputdir = '../json'
outputdir = '../frontend'
n2f_name = '_name2file.json'
name2file = parseJSON(n2f_name) if os.path.exists(n2f_name) else {}
sleigh = Sleigh(ienputdir + '/corpus', name2file)

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
		lst = [x.getItem() for x in \
			sorted(stems[k], key=lambda z: -z.json['year'] if 'year' in z.json.keys() else 0)]
		f.write(wordHTML.format(\
			title=k+' stem',
			stem=k,
			listname='{} papers'.format(len(lst)),
			dl='<dl class="toc">' + '\n'.join(lst).replace('href="', 'href="../') + '</dl>'))
		f.close()
	print('Word pages:', C.yellow('{}'.format(len(stems))), C.blue('generated'))
	# stem index
	f = open(outputdir+'/words.html', 'w')
	# TODO: add length mod
	keyz = [k for k in stems.keys() if (len(k) > 10 or len(k) < 4) and k not in trash]
	keyz.sort(key=lambda t: -len(t), reverse=True)
	lst = ['<li>$<a href="word/{}.html">{}</a> ({})</li>'.format(\
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
