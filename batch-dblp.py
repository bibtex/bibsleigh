#!/c/Users/vadim/AppData/Local/Programs/Python/Python35/python
# -*- coding: utf-8 -*-
#
# a module for importing DBLP data straight from the pages into LRJs

import sys, time, socket, os, os.path, random
import bs4
from urllib.request import urlopen
from lib.JSON import jsonkv, jsonify
from lib.LP import lastSlash

def xml2json(x):
	jsonmap = {}
	s = bs4.BeautifulSoup(x)
	for main in s.dblp.children:
		if isinstance(main, bs4.element.NavigableString):
			continue
		jsonmap['type'] = main.name
		if main.has_attr('key'):
			jsonmap['dblpkey'] = main.attrs['key']
		for t in main.children:
			if isinstance(t, bs4.element.NavigableString):
				continue
			if t.name in jsonmap:
				if not isinstance(jsonmap[t.name], list):
					jsonmap[t.name] = [jsonmap[t.name], t.text]
				else:
					jsonmap[t.name].append(t.text)
			else:
				jsonmap[t.name] = t.text
	if 'title' in jsonmap:
		jsonmap['title'] = jsonmap['title'].strip()
		if jsonmap['title'].endswith('.'):
			jsonmap['title'] = jsonmap['title'][:-1]
		# if jsonmap['title'].find('roceedings') < 0:
		# 	jsonmap['title'] = '{' + jsonmap['title'] + '}'
	# return '{\n\t'+',\n\t'.join([jsonkv(k, jsonmap[k]) for k in jsonmap])+'\n}'
	return jsonify(jsonmap)

def purenameof(f):
	return lastSlash(f)[:-4]

def safelyLoadURL(url):
	time.sleep(random.randint(1, 3))
	errors = 0
	while errors < 3:
		try:
			return urlopen(url).read().decode('utf-8')
		except IOError:
			print('Warning: failed to load URL, retrying...')
			errors += 1
		except socket.error:
			print('Warning: connection reset by peer, retrying...')
			time.sleep(random.randint(10, 30))
			errors += 1
	print('Error fetching URL: ' + url)
	return ''

if __name__ == "__main__":
	if len(sys.argv) not in (3, 4):
		print('Usage:\n\t{} <URI> <VENUE>'.format(sys.argv[0]))
		sys.exit(1)
	url = sys.argv[1]
	venue = sys.argv[2]
	dblp = safelyLoadURL(url)
	# dblp = open('/Users/zaytsev/Desktop/dblp.html' ,'r', encoding='utf-8').read()
	# http://dblp.uni-trier.de/db/conf/cbse/
	links = [a[a.rindex('"')+1:] for a in dblp.split('">[contents]</a>')[:-1]]
	f = open('batch', 'w', encoding='utf-8')
	f.write('#!/bin/sh\n\n')
	for lnk in links:
		# http://dblp.uni-trier.de/db/conf/cbse/cbse2015.html
		name = ''
		year = ''
		for c in lnk[lnk.rindex('/')+1:lnk.rindex('.')]:
			if c.isdigit():
				year += c
			else:
				name += c
		name = name.upper()
		f.write('./import-dblp.py {url} ../json/corpus/{ven}/{year}/{ed}-{year}\n'.format(\
			url=lnk,
			ven=venue,
			ed=name,
			year=year))
	f.close()
	print(len(links), 'imports scheduled.')
