#!/usr/local/bin/python3

import sys, time, socket, os, os.path, random
import bs4
from urllib.request import urlopen

def jsonify(s):
	if isinstance(s, str):
		if s.isdigit():
			return s
		else:
			return '"'+s+'"'
	elif isinstance(s, list):
		return '[' + ', '.join([jsonify(x) for x in s]) + ']'
	else:
		print('Unknown JSON type in', s)
		return '"'+s+'"'

def jsonkv(k, v):
	return jsonify(k) + ': ' + jsonify(v)

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
		if jsonmap['title'].find('roceedings') < 0:
			jsonmap['title'] = '{' + jsonmap['title'] + '}'
	return '{\n\t'+',\n\t'.join([jsonkv(k, jsonmap[k]) for k in jsonmap])[:-1]+'\n}'

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
			errors += 1
	print('Error fetching URL: ' + url)
	return ''

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print('Usage:\n\tdblp2json.py <URI> <DIR>')
		print('e.g.: ./dblp2json.py http://dblp.uni-trier.de/db/conf/sigplan/sigplan82.html ../json/PLDI/1982/SCC-1982')
		sys.exit(1)
	dblp = safelyLoadURL(sys.argv[1])
	ldir = sys.argv[2]
	allxmls = [xmlname for xmlname in dblp.split('"') if xmlname.endswith('.xml')]
	if not os.path.exists(ldir):
		os.makedirs(ldir)
	ps = 0
	for xmlname in allxmls:
		print('\tFetching ' + xmlname)
		ps += 1
		xml = safelyLoadURL(xmlname)
		if xmlname.split('/')[-1].split('.')[0].isdigit():
			print('\t\tAssumed to be the boss record!')
			lname = ldir + '.json'
		else:
			qname = ldir.split('/')[-1]
			lname = ldir + '/' + qname + '-' + xmlname.split('/').replace('.xml', '.json')
		while os.path.isfile(lname):
			lname += '_'
		# now write!
		g = open(lname, 'w')
		g.write(xml2json(xml))
		g.close()
	print('Imported {} papers.'.format(ps))
