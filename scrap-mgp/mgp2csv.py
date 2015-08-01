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

if __name__ == "__main__":
	cx = 0
	id2name = {}
	id2kids = {}
	id2advs = {}
	rel = []
	for mgid in range(0, 1000):
		cx += 1
		# soup = bs4.BeautifulSoup(open('../mgp.example.html', 'r'))
		soup = bs4.BeautifulSoup(safelyLoadURL('http://www.genealogy.ams.org/id.php?id={}'.format(mgid)))
		# soup = bs4.BeautifulSoup(open('mgp2.txt', 'r'))
		myName = soup.find_all('h2')[0].getText()
		# myId = soup.find_all('a').has_attr('href', 'http://www.genealogy.ams.org/submit-data.php?id=NEW&edit=0').findPreviousSibling()
		myId = mgid
		# soup.find_all('table')[0].findNextSibling().findNextSibling().find_all('a')[0].get('href').split('id=')[1].split('&')[0]
		if int(myId) != mgid:
			print('Strange ID mismatch of {} and {} for {}'.format(mgid, myId, myName))
			continue
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
