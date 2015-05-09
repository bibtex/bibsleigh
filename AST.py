#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import glob, os.path
from Templates import confHTML, bibHTML

# SANER
# 	2012
# 		CSMR-2012.json (bibtex on the conf page)
# 		CSMR-2012 (conf page with the list of papers)
# 			CSMR-2012-*.json (each a paper page with bibtex, each a list item on the conf page)
# 		WCRE-2012.json
# 		WCRE-2012
# 			WCRE-2012-*.json

def last(xx):
	return xx.split('/')[-1].replace('.json', '')

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
	def __init__(self, d):
		self.filename = d
		self.json = {}
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
				if isinstance(self.json[k], list):
					l = self.json[k]
				else:
					l = [self.json[k]]
				s += '\t%-10s = "%s",\n' % (k, ' and '.join(l))
			elif k in ('title', 'booktitle', 'series', 'publisher'):
				if k+'short' not in self.json.keys():
					s += '\t{0:<10} = "{{{1}}}",\n'.format(k, self.json[k])
				else:
					s += '\t{0:<10} = "{{<span id="{0}">{1}</span>}}",\n'.format(k, self.json[k])
			elif k in ('crossref', 'key', 'type'):
				pass
			elif k == 'doi':
				s += '<span id="uri">\t{0:<10} = "<a href="http://dx.doi.org/{1}">{1}</a>",\n</span>'.format(k, self.json[k])
			elif k == 'dblpkey':
				s += '\t{0:<10} = "<a href="http://dblp.uni-trier.de/db/{1}">{1}</a>",\n</span>'.format(k, self.json[k])
			elif k == 'isbn':
				s += '<span id="isbn">\t{:<10} = "{}",\n</span>'.format(k, self.json[k])
			elif k in ('ee', 'url'):
				s += '<span id="uri">\t{0:<10} = "<a href=\"{1}\">{1}</a>",\n</span>'.format(k, self.json[k])
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

class Venue(Unser):
	def __init__(self, d):
		super(Venue, self).__init__(d)
		self.years = []
		for f in glob.glob(d+'/*'):
			if f.endswith('.json'):
				self.json = parseJSON(f)
			elif os.path.isdir(f):
				self.years.append(Year(f))
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
		eds = [y.getItem() for y in sorted(self.years, reverse=True, key=lambda x:x.year)]
		return confHTML.format(title=ABBR, img=img, fname=('{} ({})'.format(title, ABBR)), dl=''.join(eds))
	def getConfs(self):
		res = []
		for y in self.years:
			res.extend(y.confs)
		return res

class Year(Unser):
	def __init__(self, d):
		super(Year, self).__init__(d)
		self.year = last(d)
		self.confs = []
		for f in glob.glob(d+'/*'):
			if os.path.isdir(f):
				self.confs.append(Conf(f))
				if os.path.exists(f+'.json'):
					self.confs[-1].json = parseJSON(f+'.json')
					# print('Conf has a JSON! %s' % self.confs[-1].json)
			elif f.endswith('.json'):
				pass
			else:
				print('File out of place:', f)
	def numOfPapers(self):
		return sum([c.numOfPapers() for c in self.confs])
	def getItem(self):
		return '<dt>{}</dt>{}'.format(self.year, '\n'.join([c.getItem() for c in self.confs]))

class Conf(Unser):
	def __init__(self, d):
		super(Conf, self).__init__(d)
		self.papers = []
		for f in glob.glob(d+'/*'):
			if os.path.isfile(f) and f.endswith('.json'):
				self.papers.append(Paper(f))
			else:
				print('File or directory out of place:', f)
	def numOfPapers(self):
		return len(self.papers)
	def getItem(self):
		return '<dd><a href="{}.html">{}</a> ({} {})</dd>'.format(self.get('name'), self.get('title'), self.get('venue') , self.get('year'))
	def getPage(self):
		return bibHTML.format(
			title=self.get('title'),
			img=self.get('venue').lower(), # geticon?
			authors=self.getAuthors(),
			# self.getKey(),
			# self.getKey(),
			# fulltitle=self.get('title'),
			short='{}, {}'.format(self.get('venue'), self.get('year')),
			code=self.getCode(), #code
			bib=self.getBib(), #bib
			contents='\n'.join([p.getItem() for p in self.papers])
			)
	def getAuthors(self):
		if 'author' in self.json.keys():
			if isinstance(self.json['author'], list):
				return ', '.join(self.json['author'])
			else:
				return self.json['author']
		elif 'editor' in self.json.keys():
			if isinstance(self.json['editor'], list):
				return ', '.join(self.json['editor'])+' (editors)'
			else:
				return self.json['editor']+' (editor)'
		else:
			return ''

class Paper(Unser):
	def __init__(self, f):
		super(Paper, self).__init__(f)
		self.json = parseJSON(f)
	def getItem(self):
		return '?'
