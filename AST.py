#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import glob, os.path
from Templates import confHTML, bibHTML

def sortbypages(z):
	try:
		return int(z.get('pages').split('-')[0])
	except:
		return 0

def last(xx):
	return xx.split('/')[-1].replace('.json', '')

def listify(y):
	return y if isinstance(y, list) else [y]

def parseJSON(fn):
	dct = {}
	f1 = open(fn, 'r')
	for line in f1.readlines():
		line = line.strip()
		if line in ('{', '}', ''):
			continue
		perq = line.split('"')
		if len(perq) == 5:
			dct[perq[1]] = perq[3]
		elif len(perq) == 3 and perq[1] == 'year':
			dct[perq[1]] = int(perq[-1][2:-1])
		elif len(perq) > 5:
			dct[perq[1]] = [z for z in perq[3:-1] if z != ', ']
		else:
			print('Skipped line', line, 'in', fn)
	f1.close()
	dct['FILE'] = fn
	return dct

class Unser(object):
	def __init__(self, d, hdir):
		self.filename = d
		self.homedir = hdir
		self.json = {}
	def getPureName(self):
		# +1 for the slash
		return self.filename[len(self.homedir)+1:]
	def getJsonName(self):
		s = self.getPureName()
		return s if s.endswith('.json') else s+'.json'
	def get(self, name):
		return self.json[name] if name in self.json.keys() else self.getKey()
	def getKey(self):
		return last(self.filename)
	def getBib(self):
		if len(self.json) < 1:
			return '@misc{EMPTY,}'
		s = '@%s{%s,\n' % (self.get('type'), self.getKey())
		for k in sorted(self.json.keys()):
			if k == k.upper() or k.endswith('short'):
				# secret key
				continue
			if k in ('author', 'editor'):
				s += '\t{:<10} = "{}",\n'.format(k, ' and '.join(listify(self.json[k])))
			elif k in ('title', 'booktitle', 'series', 'publisher'):
				if k+'short' not in self.json.keys():
					s += '\t{0:<10} = "{{{1}}}",\n'.format(k, self.json[k])
				else:
					s += '\t{0:<10} = "{{<span id="{0}">{1}</span>}}",\n'.format(k, self.json[k])
			elif k in ('crossref', 'key', 'type', 'venue', 'eventtitle'):
				pass
			elif k == 'doi':
				s += '<span class="uri">\t{0:<10} = "<a href="http://dx.doi.org/{1}">{1}</a>",\n</span>'.format(k, self.json[k])
			elif k == 'dblpkey':
				# s += '\t{0:<10} = "<a href="http://dblp.uni-trier.de/db/{1}">{1}</a>",\n</span>'.format(k, self.json[k])
				s += '\t{0:<10} = "<a href="http://dblp.uni-trier.de/rec/html/{1}">{1}</a>",\n</span>'.format(k, self.json[k])
			elif k == 'isbn':
				s += '<span id="isbn">\t{:<10} = "{}",\n</span>'.format(k, self.json[k])
			elif k in ('ee', 'url'):
				for e in listify(self.json[k]):
					s += '<span class="uri">\t{0:<10} = "<a href=\"{1}\">{1}</a>",\n</span>'.format(k, e)
			else:
				s += '\t{0:<10} = "{1}",\n'.format(k, self.json[k])
		s += '}'
		return s.replace('<i>', '\\emph{').replace('</i>', '}')
	def getCode(self):
		code = ''
		for tag in ('title', 'booktitle', 'series', 'publisher'):
			if tag in self.json.keys() and tag+'short' in self.json.keys():
				code += "$('#"+tag+"').text(this.checked?'%s':'%s');" % (self.json[tag], self.json[tag+'short'])
		return code
	def getAuthors(self):
		if 'author' in self.json.keys():
			return ', '.join(listify(self.json['author']))
		elif 'editor' in self.json.keys():
			return ', '.join(listify(self.json['editor']))
		else:
			return ''

class Venue(Unser):
	def __init__(self, d, hdir):
		super(Venue, self).__init__(d, hdir)
		self.years = []
		for f in glob.glob(d+'/*'):
			if f.endswith('.json'):
				self.json = parseJSON(f)
			elif os.path.isdir(f):
				self.years.append(Year(f, self.homedir))
			else:
				print('File out of place:', f)
	def numOfPapers(self):
		return sum([y.numOfPapers() for y in self.years])
	def getItem(self):
		ABBR = self.get('name')
		title = self.get('title')
		# TO-DO: check if img exists
		return '<div class="pic"><a href="{ABBR}.html" title="{title}"><img src="stuff/{abbr}.png" alt="{title}"><br/>{ABBR}</a></div>'.format(ABBR=ABBR, abbr=ABBR.lower(), title=title)
	def getPage(self):
		ABBR = self.get('name')
		title = self.get('title')
		img = ABBR.lower()
		eds = [y.getItem() for y in sorted(self.years, reverse=True, key=lambda x: x.year)]
		return confHTML.format(\
			filename=self.getPureName(),\
			title=ABBR,\
			img=img,\
			fname=('{} ({})'.format(title, ABBR)),\
			dl=''.join(eds))
	def getConfs(self):
		res = []
		for y in self.years:
			res.extend(y.confs)
		return res

class Year(Unser):
	def __init__(self, d, hdir):
		super(Year, self).__init__(d, hdir)
		self.year = last(d)
		self.confs = []
		for f in glob.glob(d+'/*'):
			if os.path.isdir(f):
				self.confs.append(Conf(f, self.homedir))
				if os.path.exists(f+'.json'):
					self.confs[-1].json = parseJSON(f+'.json')
					# print('Conf has a JSON! %s' % self.confs[-1].json)
				self.confs[-1].year = self.year
			elif f.endswith('.json'):
				pass
			else:
				print('File out of place:', f)
	def numOfPapers(self):
		return sum([c.numOfPapers() for c in self.confs])
	def getItem(self):
		return '<dt>{}</dt>{}'.format(self.year, '\n'.join([c.getItem() for c in self.confs]))

class Conf(Unser):
	def __init__(self, d, hdir):
		super(Conf, self).__init__(d, hdir)
		self.papers = []
		self.year = 0
		for f in glob.glob(d+'/*'):
			if os.path.isfile(f) and f.endswith('.json'):
				self.papers.append(Paper(f, self.homedir))
			else:
				print('File or directory out of place:', f)
	def numOfPapers(self):
		return len(self.papers)
	def getEventTitle(self):
		if 'eventtitle' in self.json.keys():
			return self.json['eventtitle']
		elif 'booktitle' in self.json.keys():
			return '{} {}'.format(self.json['booktitle'], self.year)
		elif 'venue' in self.json.keys():
			return '{} {}'.format(self.json['venue'], self.year)
		else:
			return self.getKey().replace('-', ' ')
	def getItem(self):
		return '<dd><a href="{}.html">{}</a> ({})</dd>'.format(self.get('name'), self.get('title'), self.getEventTitle())
	def getPage(self):
		return bibHTML.format(\
			filename=self.getJsonName(),
			title=self.get('title'),
			img=self.get('venue').lower(), # geticon?
			authors=self.getAuthors(),
			short='{}, {}'.format(self.get('booktitle'), self.get('year')),
			code=self.getCode(),
			bib=self.getBib(),
			contents='<h3>Contents ({} items)</h3><dl class="toc">'.format(len(self.papers))+\
				'\n'.join([p.getItem() for p in sorted(self.papers, key=sortbypages)])+'</dl>'\
			)

class Paper(Unser):
	def __init__(self, f, hdir):
		super(Paper, self).__init__(f, hdir)
		self.json = parseJSON(f)
	def getItem(self):
		return '<dt><a href="{0}.html">{0}</a></dt><dd>{1}{2}{3}.</dd>'.format(\
			self.getKey(), self.get('title'), self.getAbbrAuthors(), self.getPages())
	def getAbbrAuthors(self):
		# <abbr title="Rainer Koschke">RK</abbr>
		if 'author' not in self.json.keys():
			return ''
		return ' ('+', '.join(['<abbr title="{0}">{1}</abbr>'.format(a,\
			''.join([w[0] for w in a.replace('-',' ').split(' ') if w]))\
			for a in listify(self.json['author'])])+')'
	def getPages(self):
		if 'pages' not in self.json.keys():
			return ''
		ps = self.json['pages'].split('-')
		if len(ps) == 3 and ps[1] == '':
			ps = [ps[0], ps[2]]
		if len(ps) != 2:
			return ', pp. {}???'.format(self.json['pages'])
		elif ps[0] == ps[1]:
			return ', p. {}'.format(ps[0])
		else:
			return ', pp. {}–{}'.format(*ps)
	def getPage(self):
		return bibHTML.format(\
			filename=self.getJsonName(),
			title=self.get('title'),
			img=self.get('venue').lower(), # geticon?
			authors=self.getAuthors(),
			short='{}, {}'.format(self.get('venue'), self.get('year')),
			code=self.getCode(),
			bib=self.getBib(),
			contents=''\
			)
