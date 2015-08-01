#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for scraping MGP into a CVS database

import bs4, sys
from urllib.request import urlopen

def clean(s):
	return s.replace('  ', ' ').strip()

def safelyLoadURL(url):
	# time.sleep(random.randint(1, 3))
	errors = 0
	while errors < 3:
		try:
			return urlopen(url).read().decode('utf-8')
		except IOError:
			print('Warning: failed to load URL, retrying...')
			errors += 1
		except socket.error:
			print('Warning: connection reset by peer, retrying...')
			time.sleep(random.randint(1, 3))
			errors += 1
	print('Error fetching URL: ' + url)
	return ''

def getme(frm, cla):
	hopefully = frm.find_all('span', class_=cla)
	return hopefully[0].getText() if hopefully else ''

if __name__ == "__main__":
	if len(sys.argv) not in (3, 5):
		print('Usage:\n\t{} <URI> <DIR> [<FROM> <TO>]'.format(sys.argv[0]))
		print(('e.g.: {} http://ceur-ws.org/Vol-1354/' + \
			'../json/corpus/SATToSE/2014/SATToSE-2014/').format(sys.argv[0]))
		sys.exit(1)
	cx = 0
	soup = bs4.BeautifulSoup(open('ceur.example.txt', 'r'))
	# soup = bs4.BeautifulSoup(safelyLoadURL('http://www.genealogy.ams.org/id.php?id={}'.format(mgid)))
	# git = lambda c: soup.find_all('span', class_=c)[0].getText()
	gits = lambda c: [e.getText() for e in soup.find_all('span', class_=c)]
	volNr = getme(soup, 'CEURVOLNR')
	volUrn = getme(soup, 'CEURURN')
	volYear = getme(soup, 'CEURPUBYEAR')
	volAbbr = getme(soup, 'CEURVOLACRONYM')
	hope = soup.find_all('span', class_='CEURVOLACRONYM')[0].parent
	volLnk = hope.get('href') if hope.name == 'a' else ''
	volTitles = getme(soup, 'CEURVOLTITLE'), getme(soup, 'CEURFULLTITLE')
	volLocTime = getme(soup, 'CEURLOCTIME')
	volEds = getme(soup, 'CEURVOLEDITOR')

	print(volNr, volUrn, volYear, volLnk, volTitles, volEds)
	mainEntry = {'type': 'proceedings', 'series': 'CEUR Workshop Proceedings', 'publisher': 'CEUR-WS.org',
		'year': volYear, 'title': volTitles[-1], 'editor': volEds, 'volume': volNr.split('-')[-1],
		'urn': volUrn}
	if volLnk:
		mainEntry['url'] = [volLnk, sys.argv[1]]
	else:
		mainEntry['url'] = sys.argv[1]
	print(mainEntry)
	for li in soup.find_all(class_='CEURTOC')[0].find_all('li'):
		paperTitle = getme(li, 'CEURTITLE')
		paperPages = getme(li, 'CEURPAGES')
		paperAuths = getme(li, 'CEURAUTHORS').split(', ')
		if paperAuths[-1].find(' and ') > -1:
			auths = [a for a in paperAuths[-1].split(' and ') if a]
			paperAuths = paperAuths[:-1]
			paperAuths.extend(auths)
		paperLnk = li.get('id')
		hope = li.find_all('a')
		if hope and hope[0].get('href').endswith('.pdf'):
			paperPdf = hope[0].get('href')
		else:
			paperPdf = ''
		if not paperTitle:
			continue
		paperEntry = {'type': 'inproceedings', 'series': 'CEUR Workshop Proceedings', 'publisher': 'CEUR-WS.org',
			'year': volYear, 'booktitle': volTitles[-1], 'editor': volEds, 'volume': volNr.split('-')[-1],
			'title': paperTitle, 'author': paperAuths, 'pages': paperPages, 'url': ''}
		if paperPdf:
			paperEntry['openpdf'] = paperPdf
		print(paperEntry)
	sys.exit(1)
	# myId = soup.find_all('a').has_attr('href', 'http://www.genealogy.ams.org/submit-data.php?id=NEW&edit=0').findPreviousSibling()
	myId = mgid
	# soup.find_all('table')[0].findNextSibling().findNextSibling().find_all('a')[0].get('href').split('id=')[1].split('&')[0]
	if int(myId) != mgid:
		print('Strange ID mismatch of {} and {} for {}'.format(mgid, myId, myName))
	print('[{}] Scraping {}'.format(myId, clean(myName)))
	myTitle = soup.find_all(id='thesisTitle')[0].getText()
	div = soup.find_all(id='thesisTitle')[0].parent.findPreviousSibling('div')
	base = div.find_all('span')
	mySchool = base[1].getText()
	myDegree, myYear = base[0].getText().split(mySchool)
	myCountry = div.find_all('img')[0].get('alt')
	id2name[myId] = list(map(clean, [myName, myDegree, myTitle, myCountry, mySchool, myYear]))
	# get advisors
	for adv in soup.find_all(id='thesisTitle')[0].parent.findNextSibling('p').find_all('a'):
		advID = adv.get('href').split('id=')[1]
		advName = adv.getText().strip()
		if myId not in id2advs.keys():
			id2advs[myId] = []
		id2advs[myId].append((advID, clean(advName)))
	# get descendants
	if soup.find_all('table'):
		tds = soup.find_all('table')[0].find_all('td')
		for i in range(len(tds)//4):
			childID = tds[4*i].find_all('a')[0].get('href').split('=')[-1]
			childName = tds[4*i].getText().strip()
			childSchool = tds[4*i+1].getText().strip()
			childYear = tds[4*i+2].getText().strip()
			if myId not in id2kids.keys():
				id2kids[myId] = []
			id2kids[myId].append((childID, childName, childSchool, childYear))
	f = open('_id2name.csv', 'a')
	print('============================== ID -> NAME: ==============================')
	for i in sorted(id2name.keys(), key=lambda n: int(n)):
		nm = id2name[i]
		s = '{};{};{};{};{};{};{}'.format(i, nm[0], nm[1], nm[2], nm[3], nm[4], nm[5])
		print(s)
		f.write(s+'\n')
	f.close()
	f = open('_id2kids.csv', 'a')
	print('============================== ID -> KIDS: ==============================')
	for i in sorted(id2kids.keys(), key=lambda n: int(n)):
		for kid in id2kids[i]:
			s = '{};{};{};{};{};{}'.format(i, id2name[i][0], kid[0], kid[1], kid[2], kid[3])
			print(s)
			f.write(s+'\n')
			if (i, kid[0]) not in rel:
				rel.append((i, kid[0]))
	f.close()
	f = open('_id2adv.csv', 'a')
	print('============================== ID -> ADVS: ==============================')
	for i in sorted(id2advs.keys(), key=lambda n: int(n)):
		for adv in id2advs[i]:
			s = '{};{};{};{}'.format(i, id2name[i][0], adv[0], adv[1])
			print(s)
			f.write(s+'\n')
			if (adv[0], i) not in rel:
				rel.append((adv[0], i))
	f.close()
	print('=========================================================================')
	print('Imported {} mathematicians and {} relations among them.'.format(cx, len(rel)))
