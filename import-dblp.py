#!/c/Users/vadim/AppData/Local/Programs/Python/Python37-32/python
# -*- coding: utf-8 -*-
#
# a module for importing DBLP data straight from the pages into LRJs

import sys, time, socket, os, os.path, random
import bs4
from urllib.request import urlopen
from lib.JSON import jsonkv, jsonify
from lib.LP import lastSlash
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

def xml2json(x):
	jsonmap = {}
	s = bs4.BeautifulSoup(x, 'html.parser')
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
	# time.sleep(random.randint(1, 3))
	time.sleep(1)
	errors = 0
	while errors < 3:
		try:
			return urlopen(url, context=ctx).read().decode('utf-8')
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
	if len(sys.argv) not in (3, 5):
		print('Usage:\n\t{} <URI> <DIR> [<FROM> <TO>]'.format(sys.argv[0]))
		print(('e.g.: {} http://dblp.uni-trier.de/db/conf/sigplan/sigplan82.html' + \
			'../json/corpus/PLDI/1982/SCC-1982').format(sys.argv[0]))
		sys.exit(1)
	dblp = safelyLoadURL(sys.argv[1])
	tmp = open('httpdump.raw', 'w')
	tmp.write(dblp)
	tmp.close()
	ldir = sys.argv[2]
	year = ldir.split('/')[4]
	allxmls = [xmlname for xmlname in dblp.split('"') if xmlname.endswith('.xml')]
	if len(sys.argv) == 5:
		entry1 = lastSlash(sys.argv[3])
		entry2 = lastSlash(sys.argv[4])
	else:
		entry1 = purenameof(allxmls[0])
		entry2 = purenameof(allxmls[-1])
	if not os.path.exists(ldir):
		os.makedirs(ldir)
	ps = 0
	yeswecan = False
	for xmlname in allxmls:
		if yeswecan:
			if purenameof(xmlname) == entry2:
				yeswecan = False
		else:
			if purenameof(xmlname) == entry1:
				yeswecan = True
			else:
				print('\tSkipping ' + xmlname)
				continue
		print('\tFetching ' + xmlname)
		ps += 1
		xml = safelyLoadURL(xmlname)
		if lastSlash(xmlname).split('.')[0].isdigit():
			print('\t\tAssumed to be the boss record!')
			lname = ldir + '.json'
		else:
			qname = lastSlash(ldir)
			lname = ldir + '/' + qname + '-' + lastSlash(xmlname).replace('.xml', '.json')
			# print('NB: match "{}" vs "{}"'.format(lname[:-5], year))
			if lname[:-5].endswith(year):
				lname = lname[:-5-len(year)] + '.json'
			if lname[:-5].endswith(year[-2:]):
				lname = lname[:-7] + '.json'
		while os.path.isfile(lname):
			lname = lname.replace('.json', '_.json')
		# now write!
		g = open(lname, 'w', encoding='utf-8')
		g.write(xml2json(xml))
		g.close()
		print('\t\t->', lname)
	print('Imported {} papers.'.format(ps))
