#!/c/Users/vadim/AppData/Local/Programs/Python/Python35/python
# -*- coding: utf-8 -*-
#
# a module for scraping MGP into a CSV database

import bs4, sys, time, socket, random, urllib.request

rel = []

def clean(s):
	return s.replace('  ', ' ').strip()

def safelyLoadURL(url):
	errors = 0
	while errors < 3:
		try:
			return urllib.request.urlopen(url, None, 5).read().decode('utf-8')
			# return urllib.request.urlopen(url).read().decode('utf-8')
		except IOError:
			print('Warning: failed to load URL, retrying...')
			errors += 1
		except socket.error:
			print('Warning: connection reset by peer, retrying...')
			time.sleep(random.randint(1, 3))
			errors += 1
	print('Error fetching URL: ' + url)
	return ''

def write_name(f, i, nm):
	s = '{};{};{};{};{};{};{}'.format(i, nm[0], nm[1], nm[2], nm[3], nm[4], nm[5])
	# print(s)
	f.write(s+'\n')
	f.flush()

def write_kids(f, i, kid, id2n):
	if not id2n[i]:
		print('\tCannot find name', i, 'for', kid)
		name = 'UNDEFINED'
	else:
		name = id2n[i][0]
	s = '{};{};{};{};{};{}'.format(i, name, kid[0], kid[1], kid[2], kid[3])
	# print(s)
	f.write(s+'\n')
	f.flush()
	if (i, kid[0]) not in rel:
		rel.append((i, kid[0]))

def write_advs(f, i, adv, id2n):
	if not id2n[i]:
		print('\tCannot find name', i, 'for', adv)
		name = 'UNDEFINED'
	else:
		name = id2n[i][0]
	s = '{};{};{};{}'.format(i, name, adv[0], adv[1])
	# print(s)
	f.write(s+'\n')
	f.flush()
	if (adv[0], i) not in rel:
		rel.append((adv[0], i))

if __name__ == "__main__":
	cx = 0
	id2name = {}
	id2kids = {}
	id2advs = {}
	f_name = open('_id2name.csv', 'a')
	f_kids = open('_id2kids.csv', 'a')
	f_advs = open('_id2adv.csv', 'a')
	startfrom = int(sys.argv[1]) if len(sys.argv) > 1 else 1
	for mgid in range(startfrom, startfrom+10000):
		cx += 1
		if cx % 100 == 0:
			print('================================= +100 =================================')
		progress = ''
		# soup = bs4.BeautifulSoup(open('../mgp.example.html', 'r'))
		soup = bs4.BeautifulSoup(safelyLoadURL('http://www.genealogy.ams.org/id.php?id={}'.format(mgid)))
		# soup = bs4.BeautifulSoup(open('mgp2.txt', 'r'))
		hope = soup.find_all('h2')
		if not hope:
			print('[{}] ID that does not exist in the database'.format(mgid))
			continue
		myName = hope[0].getText()
		# myId = soup.find_all('a').has_attr('href', 'http://www.genealogy.ams.org/submit-data.php?id=NEW&edit=0').findPreviousSibling()
		myId = mgid
		# soup.find_all('table')[0].findNextSibling().findNextSibling().find_all('a')[0].get('href').split('id=')[1].split('&')[0]
		if int(myId) != mgid:
			print('Strange ID mismatch of {} and {} for {}'.format(mgid, myId, myName))
			continue
		hope = soup.find_all(id='thesisTitle')
		if hope:
			myTitle = hope[0].getText()
			div = hope[0].parent.findPreviousSibling('div')
			base = div.find_all('span')
			hope = div.find_all('img')
			myCountry = hope[0].get('alt') if hope else '???'
			if base:
				mySchool = base[1].getText()
				# sometimes school is unknown (e.g., ID #238)
				if not mySchool:
					myYear = base[0].getText().strip()[-4:]
					myDegree = base[0].getText().replace(myYear, '').strip()
				else:
					myDegree, myYear = base[0].getText().split(mySchool)
			else:
				mySchool = '???'
				myYear = '???'
				myDegree = '???'
		else:
			myTitle = '???'
			mySchool = '???'
			myDegree = '???'
			myCountry = '???'
			myYear = '???'
		id2name[myId] = list(map(clean, [myName, myDegree, myTitle, myCountry, mySchool, myYear]))
		write_name(f_name, myId, id2name[myId])
		progress += '√'
		# get advisors
		if soup.find_all(id='thesisTitle'):
			hope = soup.find_all(id='thesisTitle')[0].parent.findNextSibling('p')
			if hope:
				for adv in hope.find_all('a'):
					advID = adv.get('href').split('id=')[1]
					advName = adv.getText().strip()
					if myId not in id2advs.keys():
						id2advs[myId] = []
					id2advs[myId].append((advID, clean(advName)))
					write_advs(f_advs, myId, id2advs[myId][-1], id2name)
					progress += '√'
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
				write_kids(f_kids, myId, id2kids[myId][-1], id2name)
				progress += '√'
		print('[{}] Harvested {} [{}]'.format(myId, clean(myName), progress))
	f_name.close()
	f_kids.close()
	f_advs.close()
	print('=========================================================================')
	print('Imported {} mathematicians and {} relations among them.'.format(cx, len(rel)))
