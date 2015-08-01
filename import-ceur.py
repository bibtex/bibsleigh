#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for harvesting a CEUR link into a proper BibSLEIGH entity

import bs4, sys, os.path, time
from urllib.request import urlopen
from lib.JSON import jsonify
from fancy.ANSI import C

def safelyLoadURL(url):
	# time.sleep(random.randint(1, 3))
	errors = 0
	while errors < 3:
		try:
			return urlopen(url).read().decode('utf-8')
		except:
			print('Warning: failed to load URL, retrying...')
			time.sleep(5)
			errors += 1
	print('Error fetching URL: ' + url)
	return ''

def getme(frm, cla):
	hopefully = [e.getText() for e in frm.find_all('span', class_=cla)]
	if len(hopefully) == 1:
		return hopefully[0]
	else:
		return hopefully
	# NB: [] is not treated differently

if __name__ == "__main__":
	if len(sys.argv) != 3:
		print('Usage:\n\t{} <URI> <DIR>'.format(sys.argv[0]))
		print(('e.g.: {} http://ceur-ws.org/Vol-1354/' + \
			'../json/corpus/SATToSE/2014/SATToSE-2014/').format(sys.argv[0]))
		sys.exit(1)
	volVenue = sys.argv[2].split('corpus/')[1].split('/')[0]
	cx = 0
	outputdir = sys.argv[2]
	if outputdir.endswith('/'):
		outputdir = outputdir[:-1]
	if not os.path.exists(outputdir):
		os.makedirs(outputdir)
	urlstart = sys.argv[1]
	if not urlstart.endswith('/'):
		urlstart += '/'
	# soup = bs4.BeautifulSoup(open('ceur.example.txt', 'r'))
	soup = bs4.BeautifulSoup(safelyLoadURL(urlstart))
	volNr = getme(soup, 'CEURVOLNR')
	volUrn = getme(soup, 'CEURURN')
	volYear = getme(soup, 'CEURPUBYEAR')
	volAbbr = getme(soup, 'CEURVOLACRONYM')
	hope = soup.find_all('span', class_='CEURVOLACRONYM')[0].parent
	volLnk = hope.get('href') if hope.name == 'a' else ''
	volTitles = getme(soup, 'CEURVOLTITLE'), getme(soup, 'CEURFULLTITLE')
	volLocTime = getme(soup, 'CEURLOCTIME')
	volEds = getme(soup, 'CEURVOLEDITOR')
	# print(volNr, volUrn, volYear, volLnk, volTitles, volEds)
	mainEntry = {'type': 'proceedings', 'series': 'CEUR Workshop Proceedings',\
		'publisher': 'CEUR-WS.org', 'year': volYear, 'title': volTitles[-1],\
		'editor': volEds, 'volume': volNr.split('-')[-1], 'urn': volUrn,\
		'ee': urlstart, 'venue': volVenue}
	if volLnk:
		mainEntry['url'] = volLnk
	# print(jsonify(mainEntry), '-->', outputdir+'.json')
	f = open(outputdir+'.json', 'w')
	f.write(jsonify(mainEntry))
	f.close()
	done = []
	for li in soup.find_all(class_='CEURTOC')[0].find_all('li'):
		paperTitle = getme(li, 'CEURTITLE')
		if not paperTitle:
			continue
		paperPages = getme(li, 'CEURPAGES')
		paperAuths = getme(li, 'CEURAUTHORS').split(', ')
		if paperAuths[-1].find(' and ') > -1:
			auths = [a for a in paperAuths[-1].split(' and ') if a]
			paperAuths = paperAuths[:-1]
			paperAuths.extend(auths)
		paperLnk = li.get('id')
		hope = li.find_all('a')
		if hope and hope[0].get('href').endswith('.pdf'):
			paperPdf = urlstart + hope[0].get('href')
		else:
			paperPdf = ''
		paperEntry = {'type': 'inproceedings', 'series': 'CEUR Workshop Proceedings',\
			'publisher': 'CEUR-WS.org', 'year': volYear, 'booktitle': volTitles[-1],\
			'editor': volEds, 'volume': volNr.split('-')[-1], 'title': paperTitle,\
			'author': paperAuths, 'pages': paperPages, 'venue': volVenue}
		if paperPdf:
			paperEntry['openpdf'] = paperPdf
		if paperLnk:
			paperEntry['url'] = urlstart + '#' + paperLnk
		paperFilename = outputdir.split('/')[-1] + '-' + paperAuths[0].split(' ')[-1]
		for a in paperAuths[1:]:
			paperFilename += a.split(' ')[-1][0]
		if paperFilename in done:
			paperFilename += 'a'
			while paperFilename in done:
				paperFilename = paperFilename[:-1] + chr(ord(paperFilename[-1])+1)
		# print(jsonify(paperEntry), '-->', outputdir+'/'+paperFilename+'.json')
		f = open(outputdir+'/'+paperFilename+'.json', 'w')
		f.write(jsonify(paperEntry))
		f.close()
		cx += 1
		done.append(paperFilename)
	print(C.red(volVenue), '-', C.yellow(volTitles[-1]), '-', C.blue(cx), 'papers.')
