#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module with classes forming the abstract syntax of BibSLEIGH

import glob, os.path
from fancy.Templates import uberHTML, confHTML, bibHTML, brandHTML
from lib.JSON import jsonkv, parseJSON
from lib.LP import listify
from lib.NLP import string2words, ifApproved
from fancy.ANSI import C

def sortMyTags(tpv):
	tagPerFreq = {}
	for k in tpv.keys():
		if tpv[k] < 2:
			# top tags are those that are used more than once
			continue
		if tpv[k] not in tagPerFreq.keys():
			tagPerFreq[tpv[k]] = []
		tagPerFreq[tpv[k]].append(k)
	result = []
	for n in sorted(tagPerFreq.keys(), reverse=True):
		result.extend([[t, n] for t in sorted(tagPerFreq[n])])
	return result

def escape(s):
	for k, v in ((' ', '%20'), ('+', '%2B'), ('#', '%23')):
		s = s.replace(k, v)
	return s

# Sort first by year, then by pages
def sortbypages(z):
	if 'pages' not in z.json.keys():
		print(C.red('No pages at all in '+z.getKey()))
		return 0
	p1, _ = z.getPagesTuple()
	y = z.get('year')
	if isinstance(y, str):
		# non-correcting robustness
		return 0
	# a trick to have several volumes within one conference
	v = z.get('volume')
	if isinstance(v, int) or v.isdigit():
		y += int(v)
	return (y + p1 / 10000.) if p1 else y

def last(xx):
	return xx.split('/')[-1].replace('.json', '')

class Unser(object):
	def __init__(self, d, hdir):
		self.filename = d
		self.homedir = hdir
		self.json = {}
		self.back = self
		self.tags = None
		self.stems = None
		self.n2f = {}
	def getPureName(self):
		# +1 for the slash
		return self.filename[len(self.homedir)+1:]
	def getJsonName(self):
		s = self.getPureName()
		return s if s.endswith('.json') else s+'.json'
	def getHtmlName(self):
		s = self.getPureName().split('/')[-1]
		if s.endswith('.json'):
			s = s[:-5]
		return s if s.endswith('.html') else s+'.html'
	def get(self, name):
		return self.json[name] if name in self.json.keys() else self.getKey()
	def getKey(self):
		return last(self.filename)
	def getBib(self):
		if len(self.json) < 1:
			return '@misc{EMPTY,}'
		s = '@%s{%s,\n' % (self.get('type'), self.getKey())
		n2f = self.n2f if self.n2f else self.back.n2f
		for k in sorted(self.json.keys()):
			if k == k.upper() or k.endswith('short') or k == 'tag':
				# secret key
				continue
			if k in ('author', 'editor'):
				# TODO: add (correct!) links
				aelinks = [\
					'<a href="{}">{}</a>'.format(n2f[ae], ae)
						if ae in n2f.keys()
						else ae
					for ae in listify(self.json[k])
				]
				s += '\t{:<13} = "{}",\n'.format(k, ' and '.join(aelinks))
			elif k in ('title', 'booktitle', 'series', 'publisher', 'journal'):
				if k+'short' not in self.json.keys():
					s += '\t{0:<13} = "{{{1}}}",\n'.format(k, self.json[k])
				else:
					s += '\t{0:<13} = "{{<span id="{0}">{1}</span>}}",\n'.format(k, self.json[k])
			elif k in ('crossref', 'key', 'type', 'venue', 'twitter', \
				'eventtitle', 'eventurl', 'nondblpkey', 'dblpkey', 'dblpurl', \
				'programchair', 'generalchair', 'roles', 'tagged', 'stemmed'):
				# TODO: ban 'ee' as well
				pass
			elif k == 'doi':
				s += '<span class="uri">\t{0:<13} = "<a href="http://dx.doi.org/{1}">{1}</a>",\n</span>'.format(k, self.json[k])
			elif k == 'acmid':
				s += '<span class="uri">\t{0:<13} = "<a href="http://dl.acm.org/citation.cfm?id={1}">{1}</a>",\n</span>'.format(k, self.json[k])
			elif k == 'dblpkey':
				# Legacy!
				# s += '\t{0:<13} = "<a href="http://dblp.uni-trier.de/db/{1}">{1}</a>",\n</span>'.format(k, self.json[k])
				s += '\t{0:<13} = "<a href="http://dblp.uni-trier.de/rec/html/{1}">{1}</a>",\n'.format(k, self.json[k])
			elif k == 'isbn':
				s += '<span id="isbn">\t{:<13} = "{}",\n</span>'.format(k, self.json[k])
			elif k in ('ee', 'url'):
				for e in listify(self.json[k]):
					# VVZ: eventually would like to get rid of EE completely
					# VVZ: limiting it for now to possibly interesting cases
					if k == 'ee' and (e.startswith('http://dx.doi.org') or \
						e.startswith('http://dl.acm.org') or\
						e.startswith('http://doi.ieeecomputersociety.org')\
					):
						continue
					s += '<span class="uri">\t{0:<13} = "<a href=\"{1}\">{1}</a>",\n</span>'.format(k, e)
			elif k in ('year', 'volume', 'issue', 'number') and isinstance(self.json[k], int):
				s += '\t{0:<13} = {1},\n'.format(k, self.json[k])
			elif k == 'pages':
				s += '\t{0:<13} = "{1}",\n'.format(k, self.getPagesBib())
			elif k == 'address':
				if isinstance(self.json[k], str):
					a = self.json[k]
				elif self.json[k][1]:
					a = ', '.join(self.json[k])
				else:
					a = self.json[k][0] + ', ' + self.json[k][2]
				s += '\t{0:<13} = "{1}",\n'.format(k, a)
			else:
				s += '\t{0:<13} = "{1}",\n'.format(k, self.json[k])
		s += '}'
		return s.replace('<i>', '\\emph{').replace('</i>', '}')
	def getCode(self):
		code = ''
		for tag in ('title', 'booktitle', 'series', 'publisher', 'journal'):
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
	def getBoxLinks(self):
		links = [[], [], []]
		# Crossref to the parent
		# DOC: real crossrefs are nice, but all the global searches slows the engine down
		# DOC: (running time 5m11.559s vs 0m7.396s is 42x)
		# if 'crossref' in self.json.keys():
		# 	xref = self.top().seek(self.json['crossref'])
		# 	if xref:
		# 		links.append('<strong><a href="{}.html">{}</a></strong>'.format(\
		# 			xref.getKey(),
		# 			xref.getKey().replace('-', ' ')))
		# 	else:
		# 		links.append('Xref not found')
		# else:
		# 	links.append('no Xref')
		# DOC: instead, we just link to the parent!
		links[0].append('<strong><a href="{}.html">{}</a></strong>'.format(\
			self.up().getKey(),
			self.up().getKey().replace('-', ' ')))
		# DBLP
		if 'dblpkey' in self.json:
			for dblpk in listify(self.json['dblpkey']):
				links[1].append('<a href="http://dblp.uni-trier.de/rec/html/{}">DBLP</a>'.format(dblpk))
		elif 'dblpurl' in self.json:
			links[1].append('<a href="{}">DBLP</a>'.format(self.json['dblpurl']))
		else:
			links[1].append('no DBLP info')
		# Scholar
		if 'title' in self.json.keys():
			links[1].append('<a href="https://scholar.google.com/scholar?q=%22{}%22">Scholar</a>'.format(\
				str(self.json['title']).replace(' ', '+')))
		# Some publishers
		if 'ee' in self.json.keys():
			for e in listify(self.json['ee']):
				if e.find('http://dl.acm.org') \
				or e.startswith('http://doi.acm.org')\
				or e.startswith('http://portal.acm.org'):
					links[2].append('<a href="{}">ACM DL</a>'.format(e))
				elif e.startswith('http://ieeexplore.ieee.org'):
					links[2].append('<a href="{}">IEEE Xplore</a>'.format(e))
				elif e.startswith('http://ieeecomputersociety.org'):
					links[2].append('<a href="{}">IEEE CS</a>'.format(e))
				elif e.startswith('http://drops.dagstuhl.de'):
					links[2].append('<a href="{}">Dagstuhl</a>'.format(e))
				elif e.find('computer.org/csdl/proceedings') > 0:
					links[2].append('<a href="{}">CSDL</a>'.format(e))
				elif e.startswith('http://journal.ub.tu-berlin.de/eceasst'):
					links[2].append('<a href="{}">EC-EASST</a>'.format(e))
				elif e.startswith('http://ceur-ws.org'):
					links[2].append('<a href="{}">CEUR</a>'.format(e))
				elif e.startswith('http://dx.doi.org'):
					pass
				else:
					links[2].append('<a href="{}">?EE?</a>'.format(e))
		if 'doi' in self.json.keys():
			links[2].append('<a href="http://dx.doi.org/{}">DOI</a>'.format(self.json['doi']))
		return '<hr/>'.join(['<br/>\n'.join(lb) for lb in links if lb])
	def up(self):
		return self.back
	def top(self):
		if self == self.back:
			return self
		else:
			return self.back.top()
	def seek(self, key):
		return None
	def getJSON(self):
		# 'tag' is there, but also it isn’t
		if self.tags:
			self.json['tag'] = self.tags
		goodkeys = sorted(self.json.keys())
		if 'FILE' in goodkeys:
			goodkeys.remove('FILE')
		s = '{\n\t' + ',\n\t'.join([jsonkv(k, self.json[k]) for k in goodkeys]) + '\n}'
		if 'tag' in goodkeys:
			del self.json['tag']
		return s
	def numOfTags(self):
		return len(self.getTags())
	def getTags(self):
		return {}
	def getPagesString(self):
		p1, p2 = self.getPagesTuple()
		if not p1 and not p2:
			return ''
		elif p1 and not p2:
			return ', p. {}–?'.format(p1)
		elif p2 and not p1:
			# weird
			return ', p. ?–{}'.format(p2)
		elif p1 == p2:
			return ', p. {}'.format(p1)
		else:
			return ', pp. {}–{}'.format(p1, p2)
	def getPagesBib(self):
		p1, p2 = self.getPagesTuple()
		if p1 == p2:
			return '{}'.format(p1)
		else:
			return '{}--{}'.format(p1, p2)
	def getPagesTuple(self):
		if 'pages' not in self.json.keys():
			p1 = p2 = None
		elif isinstance(self.json['pages'], int):
			p1 = p2 = self.json['pages']
		else:
			ps = self.json['pages'].split(':')[-1].split(',')[0].split('-')
			if ps[0]:
				if ':' in ps[0]:
					p1 = int(ps[0].split(':')[-1].strip())
				elif ps[0].isdigit():
					p1 = int(ps[0])
				else:
					p1 = None
					print('STRANGE pages in', self.getKey(), ':', self.json['pages'])
			else:
				p1 = None
			if ps[-1]:
				p2 = int(ps[-1])
			else:
				p2 = None
		return (p1, p2)

class Sleigh(Unser):
	def __init__(self, idir, name2file):
		super(Sleigh, self).__init__('', idir)
		self.venues = []
		self.n2f = name2file
		jsons = {}
		for d in glob.glob(idir+'/*.json'):
			jsons[d.split('/')[-1].split('.')[0]] = d
		for d in glob.glob(idir+'/*'):
			if d.endswith('.md') or d.endswith('.json'):
				continue
			if d.split('/')[-1] not in jsons.keys():
				print(C.red('Legacy non-top definition of'), d)
				self.venues.append(Venue(d, idir, name2file, self))
			else:
				self.venues.append(Venue(d, idir, name2file, self))
	def getPage(self):
		return uberHTML.format(\
			cxDom=len(self.venues),
			cxVen=sum([len(v.brands) for v in self.venues]),
			cxPap=self.numOfPapers(),
			cxVol=self.numOfVolumes(),
			items='\n'.join([v.getItem() for v in self.venues]))
	def seek(self, key):
		f = None
		for v in self.venues:
			f = v.seek(key)
			if f:
				return f
		return f
	def seekByKey(self, key):
		f = None
		# trying a shortcut
		hv = key.split('-')[0]
		for v in self.venues:
			if v.getKey() == hv:
				# print('\tShortcut to', hv)
				f = v.seekByKey(key)
				if f:
					return f
				# else:
				# 	print('\t', C.red('...failed'))
		# bruteforce search
		# print('\tBrute force searching for', key)
		for v in self.venues:
			f = v.seekByKey(key)
			if f:
				return f
		return f
	def numOfPapers(self):
		return sum([v.numOfPapers() for v in self.venues])
	def numOfVolumes(self):
		return sum([v.numOfVolumes() for v in self.venues])
	def getTags(self):
		if not self.tags:
			self.tags = {}
			for v in self.venues:
				ts = v.getTags()
				for k in ts.keys():
					if k not in self.tags.keys():
						self.tags[k] = []
					self.tags[k].extend(ts[k])
		return self.tags
	def getStems(self):
		# the code could be shorter and nicer hierarchically, but this one is fast
		if not self.stems:
			self.stems = {}
			for v in self.venues:
				for y in v.years:
					for c in y.confs:
						for p in c.papers:
							stems = p.getStems()
							for s in stems.keys():
								if s not in self.stems.keys():
									self.stems[s] = []
								self.stems[s].append(stems[s])
		return self.stems

class Brand(Unser):
	def __init__(self, f, hdir, name2file, parent):
		super(Brand, self).__init__(f, hdir)
		self.name = last(f)
		self.confs = {}
		self.json = parseJSON(f)
		self.back = parent
	def addConf(self, year, conf):
		if year not in self.confs.keys():
			self.confs[year] = []
		self.confs[year].append(conf)
	def offer(self, year, conf):
		ckey = conf.getKey()
		for rule in listify(self.json['select']):
			if ckey.startswith(rule):
				self.addConf(year, conf)
				# print(C.red(conf.getKey()), ' was accepted by ', C.red(self.name))
				return
	def getPage(self):
		if 'eventurl' in self.json.keys():
			if 'twitter' in self.json.keys():
				ev2 = ' (<a href="https://twitter.com/{twi}">@{twi}</a>)</h3>'.format(twi=self.json['twitter'])
			else:
				ev2 = ''
			if isinstance(self.json['eventurl'], list):
				urls = ['<a href="{uri}">{uri}</a>'.format(uri=u) for u in self.json['eventurl']]
				ev = '<h3>Event series pages: ' + ', '.join(urls) + ev2
			else:
				urls = '<a href="{uri}">{uri}</a>'.format(uri=self.json['eventurl'])
				ev = '<h3>Event series page: ' + urls + ev2
		else:
			ev = ''
		ads = [c.json['address'][-1] for c in self.getConfs() if 'address' in c.json.keys()]
		if ads:
			clist = {}
			for a in ads:
				if a in clist.keys():
					clist[a] += 1
				else:
					clist[a] = 1
			adds = '<div class="rbox">' + '<br/>\n'.join(['{} × {}'.format(clist[a], a) for a in sorted(clist.keys())]) + '</div>'
		else:
			adds = ''
		if 'tagged' in self.json.keys():
			# gracious continuation
			if adds:
				adds = adds[:-6]
				toptags = '<hr/>\n'
			else:
				toptags = '<div class="rbox">'
			for t in self.json['tagged'][:10]:
				toptags += '<span class="tag">{1} ×<a href="tag/{0}.html">#{0}</a></span><br/>\n'.format(*t)
			toptags += '</div>'
		else:
			toptags = ''
		ev = adds + toptags + ev
		ABBR = self.get('name')
		title = self.get('title')
		img = self.json['venue'].lower() if 'venue' in self.json.keys() else ABBR.lower()
		eds = ['<dt>{}</dt>{}'.format(y, '\n'.join([c.getItem() for c in self.confs[y]])) \
			for y in sorted(self.confs.keys(), reverse=True)]
		# # return '<dt>{}</dt>{}'.format(self.year, '\n'.join([c.getItem() for c in self.confs]))
		# eds = [y.getItem() for y in sorted(self.years, reverse=True, key=lambda x: x.year)]
		return brandHTML.format(\
			filename=self.getJsonName(),\
			title=ABBR,\
			img=img,\
			fname=('{} ({})'.format(title, ABBR)),\
			venpage=ev,\
			parent=self.back.getKey(),\
			cxPapers=self.numOfPapers(),\
			cxIssues=len(eds),\
			dl=''.join(eds))
	def getConfs(self):
		res = []
		for y in self.confs.keys():
			res.extend(self.confs[y])
		return res
	def getQTags(self):
		# if 'tagged' not in self.json.keys():
		if True:
			tpv = {}
			for y in self.confs.keys():
				for c in self.confs[y]:
					for p in c.papers:
						for t in p.getQTags():
							if t in tpv.keys():
								tpv[t] += 1
							else:
								tpv[t] = 1
			tagged = sortMyTags(tpv)
			if tagged:
				self.json['tagged'] = tagged
			return tagged
		return self.json['tagged']
	def numOfPapers(self):
		return sum([c.numOfPapers() for y in self.confs.keys() for c in self.confs[y]])


class Venue(Unser):
	def __init__(self, d, hdir, name2file, parent):
		super(Venue, self).__init__(d, hdir)
		self.years = []
		self.brands = []
		self.n2f = name2file
		if os.path.exists(d+'.json'):
			# new style
			# print(C.blue(d), 'is new style')
			self.json = parseJSON(d+'.json')
		else:
			# legacy style
			print(C.red(d), 'is legacy style')
			self.json = []
		for f in glob.glob(d+'/*.json'):
			if not self.json:
				self.json = parseJSON(f)
			else:
				self.brands.append(Brand(f, self.homedir, name2file, self))
		for f in glob.glob(d+'/*'):
			if f.endswith('.json'):
				# already processed
				continue
			elif os.path.isdir(f):
				y = Year(f, self.homedir, name2file, self)
				self.years.append(y)
				for b in self.brands:
					for c in y.confs:
						b.offer(y.year, c)
			else:
				print('File out of place:', f)
		self.back = parent
	def numOfPapers(self):
		return sum([y.numOfPapers() for y in self.years])
	def numOfVolumes(self):
		return sum([y.numOfVolumes() for y in self.years])
	def getItem(self):
		ABBR = self.get('name')
		title = self.get('title')
		img = self.json['venue'].lower() if 'venue' in self.json.keys() else ABBR.lower()
		# TO-DO: check if img exists
		return ('<div class="pic"><a href="{ABBR}.html" title="{title}">'+\
			'<img src="stuff/{abbr}.png" alt="{title}"/><h2>{ABBR}</h2></a></div>').format(\
				ABBR=ABBR,\
				abbr=img,\
				title=title)
	def getIconItem(self):
		return self.getIconItem(self.get('title'))
	def getIconItem(self, desc):
		if 'venue' in self.json.keys():
			venue = self.json['venue']
		else:
			venue = self.json['name'].lower()
		return '<a href="{name}.html" title="{hover}"><img src="stuff/{img}.png" class="abc" alt="{title}"/></a>'.format(\
			name=self.get('name'),
			title=self.get('title'),
			hover=desc,
			img=venue)
	def getPage(self):
		if 'eventurl' in self.json.keys():
			if 'twitter' in self.json.keys():
				ev2 = ' (<a href="https://twitter.com/{twi}">@{twi}</a>)</h3>'.format(twi=self.json['twitter'])
			else:
				ev2 = ''
			if isinstance(self.json['eventurl'], list):
				urls = ['<a href="{uri}">{uri}</a>'.format(uri=u) for u in self.json['eventurl']]
				ev = '<h3>Event series pages: ' + ', '.join(urls) + ev2
			else:
				urls = '<a href="{uri}">{uri}</a>'.format(uri=self.json['eventurl'])
				ev = '<h3>Event series page: ' + urls + ev2
		else:
			ev = ''
		ads = [c.json['address'][-1] for c in self.getConfs() if 'address' in c.json.keys()]
		if ads:
			clist = {}
			for a in ads:
				if a in clist.keys():
					clist[a] += 1
				else:
					clist[a] = 1
			adds = '<div class="rbox">' + '<br/>\n'.join(['{} × {}'.format(clist[a], a) for a in sorted(clist.keys())]) + '</div>'
		else:
			adds = ''
		if 'tagged' in self.json.keys():
			# gracious continuation
			if adds:
				adds = adds[:-6]
				toptags = '<hr/>\n'
			else:
				toptags = '<div class="rbox">'
			for t in self.json['tagged'][:10]:
				toptags += '<span class="tag">{1} ×<a href="tag/{0}.html">#{0}</a></span><br/>\n'.format(*t)
			toptags += '</div>'
		else:
			toptags = ''
		ev = adds + toptags + ev
		# now brands
		brands = []
		for brand in self.brands:
			if 'venue' in brand.json.keys():
				img = brand.json['venue'].lower()
			else:
				img = brand.getKey().lower()
			brands.append('<div class="wider"><a href="{name}.brand.html"><img src="stuff/{lowname}.png" class="abc" alt="{name}" title="{longname}"></a><abbr title="{longname}">{name}</abbr></div>'.format(\
				name=brand.getKey(),\
				lowname=img,\
				longname=brand.json['title'],\
				))
		ABBR = self.get('name')
		title = self.get('title')
		img = self.json['venue'].lower() if 'venue' in self.json.keys() else ABBR.lower()
		eds = [y.getItem() for y in sorted(self.years, reverse=True, key=lambda x: x.year)]
		return confHTML.format(\
			filename=self.getJsonName(),\
			title=ABBR,\
			img=img,\
			fname=('{} ({})'.format(title, ABBR)),\
			venpage=ev,\
			cxBrands=len(brands),\
			cxPapers=self.numOfPapers(),\
			cxIssues=len(eds),\
			brands='\n'.join(brands),\
			dl=''.join(eds))
	def getConfs(self):
		res = []
		for y in self.years:
			res.extend(y.confs)
		return res
	def getBrands(self):
		return self.brands
	def seek(self, key):
		if key == self.get('dblpkey'):
			return self
		f = None
		for y in self.years:
			f = y.seek(key)
			if f:
				return f
		return f
	def seekByKey(self, key):
		f = None
		# trying a shortcut
		hy = ''.join([ch for ch in key if ch.isdigit()])
		tried = []
		for y in self.years:
			if y.year == hy:
				# print('\t\tShortcut to', hy)
				f = y.seekByKey(key)
				if f:
					return f
				else:
					# print('\t\t', C.red('...failed'))
					tried.append(y)
		# bruteforce search
		for y in self.years:
			if y in tried:
				# already sought there in an attempted shortcut
				continue
			f = y.seekByKey(key)
			if f:
				return f
		return f
	def getTags(self):
		if not self.tags:
			self.tags = {}
			for y in self.years:
				ts = y.getTags()
				for k in ts.keys():
					if k not in self.tags.keys():
						self.tags[k] = []
					self.tags[k].extend(ts[k])
		return self.tags
	def getQTags(self):
		# if 'tagged' not in self.json.keys():
		if True:
			tpv = {}
			for y in self.years:
				for c in y.confs:
					for p in c.papers:
						for t in p.getQTags():
							if t in tpv.keys():
								tpv[t] += 1
							else:
								tpv[t] = 1
			tagged = sortMyTags(tpv)
			if tagged:
				self.json['tagged'] = tagged
			return tagged
		return self.json['tagged']


class Year(Unser):
	def __init__(self, d, hdir, name2file, parent):
		super(Year, self).__init__(d, hdir)
		self.year = last(d)
		self.confs = []
		jsonsfound = []
		jsonsused = []
		for f in glob.glob(d+'/*'):
			if os.path.isdir(f):
				self.confs.append(Conf(f, self.homedir, name2file, self))
				if os.path.exists(f+'.json'):
					self.confs[-1].json = parseJSON(f+'.json')
					jsonsused.append(f+'.json')
					# print('Conf has a JSON! %s' % self.confs[-1].json)
			elif f.endswith('.json'):
				jsonsfound.append(f)
			else:
				print('File out of place:', f)
		for f in jsonsfound:
			if f not in jsonsused:
				# print('Houston, we have a JSON:', f)
				self.confs.append(Conf(f[:f.rindex('.')], self.homedir, name2file, self))
				self.confs[-1].json = parseJSON(f)
		self.back = parent
	def numOfPapers(self):
		return sum([c.numOfPapers() for c in self.confs])
	def numOfVolumes(self):
		return len(self.confs)
	def getItem(self):
		return '<dt>{}</dt>{}'.format(self.year, '\n'.join([c.getItem() for c in self.confs]))
	def seek(self, key):
		f = None
		for c in self.confs:
			f = c.seek(key)
			if f:
				return f
		return f
	def seekByKey(self, key):
		f = None
		# trying a shortcut
		hc = key[:key.rindex('-')]
		for c in self.confs:
			if c.getKey() == hc:
				# print('\t\t\tShortcut to', hc)
				f = c.seekByKey(key)
				if f:
					return f
				# else:
				# 	print('\t\t\t', C.red('...failed'))
		# bruteforce search
		for c in self.confs:
			f = c.seekByKey(key)
			if f:
				return f
		return f
	def getTags(self):
		if not self.tags:
			self.tags = {}
			for c in self.confs:
				ts = c.getTags()
				for k in ts.keys():
					if k not in self.tags.keys():
						self.tags[k] = []
					self.tags[k].extend(ts[k])
		return self.tags

class Conf(Unser):
	def __init__(self, d, hdir, name2file, parent):
		super(Conf, self).__init__(d, hdir)
		self.papers = []
		self.year = parent.year
		self.n2f = name2file
		for f in glob.glob(d+'/*'):
			if os.path.isfile(f) and f.endswith('.json'):
				self.papers.append(Paper(f, self.homedir, self))
			else:
				print('File or directory out of place:', f)
		self.back = parent
	def hyperPerson(self, p):
		if p in self.n2f.keys():
			return '<a href="{}">{}</a>'.format(self.n2f[p], p)
		else:
			return p
	def numOfPapers(self):
		return len(self.papers)
	def getEventTitle(self):
		if 'eventtitle' in self.json.keys():
			return self.json['eventtitle']
		elif 'booktitleshort' in self.json.keys():
			return '{} {}'.format(self.json['booktitleshort'], self.year)
		elif 'booktitle' in self.json.keys():
			return '{} {}'.format(self.json['booktitle'], self.year)
		elif 'venue' in self.json.keys():
			return '{} {}'.format(self.json['venue'], self.year)
		else:
			return self.getKey().replace('-', ' ')
	def getIconItem0(self):
		return self.getIconItem1(self.getEventTitle())
	def getIconItem1(self, desc):
		shorter = '{}'.format(desc).replace(' ', '')\
			.replace('Organiser', 'OrganizationCommittee')\
			.replace('Organising Chair', 'OrganizationChair')
		shorter = shorter.replace('Committee', 'Co').replace('Chair', 'Ch')\
			.replace('Program', 'Pr').replace('Organization', 'O')\
			.replace('Steering', 'S').replace('Publicity', 'Pub')\
			.replace('Editor', 'Ed').replace('Publication', 'Pbl')\
			.replace('Finance', 'Fin').replace('Challenge', 'Cha')\
			.replace('SocialMedia', 'SM').replace('General', 'G')\
			.replace('Panel', 'Pa').replace('DoctoralSymposium', 'DS')\
			.replace('Scientific', 'Sci').replace('Tutorials', 'Tu')\
			.replace('Workshop', 'Wo').replace('Satellite', 'Sa')\
			.replace('IndustrialTrack', 'In').replace('ToolTrack', 'To')\
			.replace('Briefings', 'Br').replace('ERATrack', 'ERA')\
			.replace('InPrCo', 'InCo').replace('ToPrCo', 'ToCo')\
			.replace('KeynoteSpeaker', 'KN').replace('Local', 'Lo')
		# ⌥♪?
		return self.getIconItem2(desc, shorter)
	def getIconItem2(self, longdesc, shortdesc):
		if 'venue' in self.json.keys():
			venue = self.json['venue']
		elif 'venue' in self.up().json.keys():
			venue = self.up().json['venue']
		else:
			venue = 'bibsleigh'
		return '<div><a href="{name}.html" title="{title}"><img src="stuff/{img}.png" class="abc" alt="{title}"/></a><abbr title="{hover}">{abbr}</abbr></div>'.format(\
			name=self.get('name'),
			title=self.getEventTitle(),
			hover=longdesc,
			abbr=shortdesc,
			img=venue.lower())
	def getItem(self):
		icon = '<img src="stuff/{}.png" alt="{}"/>'.format(self.json['venue'].lower(), self.json['venue'])\
			if 'venue' in self.json.keys() else ''
		return '<dd>{0}<a href="{1}.html">{2}</a> ({3})</dd>'.format(\
			icon,\
			self.get('name'),\
			self.get('title'),\
			self.getEventTitle())
	def getPage(self):
		if 'eventurl' in self.json.keys():
			if 'twitter' in self.json.keys():
				ev = '<h3>Event page: <a href="{uri}">{uri}</a> (<a href="https://twitter.com/{twi}">@{twi}</a>)</h3>'.format(uri=self.json['eventurl'], twi=self.json['twitter'])
			else:
				ev = '<h3>Event page: <a href="{uri}">{uri}</a></h3>'.format(uri=self.json['eventurl'])
		else:
			ev = ''
		if 'roles' in self.json.keys():
			rolemap = {}
			for n, r in self.json['roles']:
				if r not in rolemap.keys():
					rolemap[r] = []
				rolemap[r].append(n)
			positions = []
			for r in rolemap.keys():
				if len(rolemap[r]) == 1:
					positions.append('<li><strong>{}</strong>: {}</li>'.format(r, self.hyperPerson(rolemap[r][0])))
				else:
					positions.append('<li><strong>{}</strong>: {}</li>'.format(r.replace('Chair', 'Chairs'), ', '.join([self.hyperPerson(p) for p in rolemap[r]])))
			# positions = [(c, 'General Chair') for c in listify(self.json['generalchair'])] \
			#           + [(c, 'Program Chair') for c in listify(self.json['programchair'])]
			if positions:
				ev += '<h3>Committee</h3>' + '\n'.join(positions)
			# ev += '<h3>Committee: ' + ', '.join(['<a href="person/{}.html">{}</a> ({})'.format(\
			# 	c.replace(' ', '_'),
			# 	c, t) for c, t in positions]) + '</h3>'
		if 'tagged' in self.json.keys():
			# HACK
			if not isinstance(self.json['tagged'][0], list):
				self.json['tagged'] = [self.json['tagged']]
			toptags = '<div class="rbox">'
			for t in self.json['tagged'][:10]:
				toptags += '<span class="tag">{1} ×<a href="tag/{0}.html">#{0}</a></span><br/>'.format(*t)
			toptags += '</div>'
		else:
			toptags = ''
		if self.papers:
			ev += '<h3>Contents ({} items)</h3><dl class="toc">'.format(len(self.papers))+\
				  toptags + \
				  '\n'.join([p.getItem() for p in sorted(self.papers, key=sortbypages)])+'</dl>'
		return bibHTML.format(\
			filename=self.getJsonName(),
			title=self.get('title'),
			stemmedTitle=self.get('title'),
			img=self.get('venue').lower(), # geticon?
			authors=self.getAuthors(),
			short='{}, {}'.format(self.get('booktitle'), self.get('year')),
			code=self.getCode(),
			bib=self.getBib(),
			boxlinks=self.getBoxLinks(),
			contents=ev \
			)
	def up(self):
		return self.back.up()
	def seek(self, key):
		if key == self.get('dblpkey'):
			return self
		f = None
		for p in self.papers:
			f = p.seek(key)
			if f:
				return f
		return f
	def seekByKey(self, key):
		if key == self.getKey():
			return self
		f = None
		for p in self.papers:
			f = p.seekByKey(key)
			if f:
				return f
		return f
	def getTags(self):
		if not self.tags:
			self.tags = {}
			for p in self.papers:
				ts = p.getTags()
				for k in ts.keys():
					if k not in self.tags.keys():
						self.tags[k] = []
					self.tags[k].append(ts[k])
		return self.tags
	def getQTags(self):
		# if 'tagged' not in self.json.keys():
		if True:
			tpi = {}
			for p in self.papers:
				for k in p.getQTags():
					if k in tpi.keys():
						tpi[k] += 1
					else:
						tpi[k] = 1
			tagged = sortMyTags(tpi)
			if tagged:
				self.json['tagged'] = tagged
			return tagged
		return self.json['tagged']

class Paper(Unser):
	def __init__(self, f, hdir, parent):
		super(Paper, self).__init__(f, hdir)
		self.json = parseJSON(f)
		# NB: self.tags is a list in Paper, but a dict in all other classes
		if 'tag' in self.json.keys():
			if isinstance(self.json['tag'], list):
				self.tags = self.json['tag']
			else:
				self.tags = [self.json['tag']]
			del self.json['tag']
		self.back = parent
	def getItemWTags(self, tgz, doicon):
		p1,p2 = self.getPagesTuple()
		bar = '<div class="pagevis" style="width:{}px"></div>'.format(p2-p1) if p1 and p2 else ''
		if doicon and 'venue' in self.json.keys():
			ven = '<img src="../stuff/{}.png" alt="{}"/>'.format(\
				self.json['venue'].lower(),\
				self.json['venue'])
		else:
			ven = ''
		return '<dt>{5}<a href="{0}.html">{0}</a>{4}</dt><dd>{1}{2}{3}.</dd>{6}'.format(\
			self.getKey(),\
			self.get('title').replace('&', '&amp;'),\
			self.getAbbrAuthors(),\
			self.getPagesString(),
			tgz,
			ven,
			' '+bar)
	def getItem(self):
		return self.getItemWTags(self.getFancyTags(self.tags) if self.tags else '', False)
	def getIItem(self):
		return self.getItemWTags(self.getFancyTags(self.tags) if self.tags else '', True)
	def getRestrictedItem(self, t):
		if not self.tags:
			return self.getItemWTags('', True)
		else:
			ts = self.tags[:]
			if t in ts:
				ts.remove(t)
			return self.getItemWTags(self.getFancyTags(ts), True)
	def getFancyTags(self, ts):
		# TODO: do the same backlinks for bundles
		return ' ' + ' '.join(['<span class="tag"><a href="tag/{0}.html" title="{1}">#{1}</a></span>'.format(\
			escape(t), t) for t in ts])
	def getAbbrAuthors(self):
		# <abbr title="Rainer Koschke">RK</abbr>
		if 'author' not in self.json.keys():
			return ''
		return ' ('+', '.join(['<abbr title="{0}">{1}</abbr>'.format(a,\
			''.join([w[0] for w in a.replace('-', ' ').split(' ') if w]))\
			for a in listify(self.json['author'])])+')'
	def getPage(self):
		if self.getTags():
			cnt = '<h3>Tags:</h3><ul class="tri">'
			cnt += '\n'.join(['<li class="tag"><a href="tag/{}.html">#{}</a></li>'.format(escape(t), t) for t in self.tags])
			cnt += '</ul><hr/>'
		else:
			cnt = ''
		if 'stemmed' in self.json.keys():
			title = self.get('title')
			ltitle = title.lower()
			words = string2words(title)
			words.reverse()
			fancytitle = ''
			for w in words:
				i = ltitle.rindex(w)
				stem = self.json['stemmed'][len(words) - words.index(w)-1]
				if ifApproved(stem):
					fancytitle = '<a href="word/{}.html">{}</a>{}'.format(\
						stem, title[i:i+len(w)], title[i+len(w):]) + fancytitle
				else:
					fancytitle = title[i:] + fancytitle
				ltitle = ltitle[:i]
				title = title[:i]
			fancytitle = title + fancytitle
		else:
			fancytitle = self.get('title')
		return bibHTML.format(\
			filename=self.getJsonName(),
			title=self.get('title'),
			stemmedTitle=fancytitle,
			img=self.get('venue').lower(), # geticon?
			authors=self.getAuthors(),
			short='{}, {}'.format(self.get('venue'), self.get('year')),
			code=self.getCode(),
			bib=self.getBib(),
			boxlinks=self.getBoxLinks(),
			contents=cnt\
			)
	def seek(self, key):
		if key == self.get('dblpkey'):
			return self
		else:
			return None
	def seekByKey(self, key):
		if key == self.getKey():
			return self
		else:
			return None
	def getTags(self):
		return {k:self for k in self.tags} if self.tags else {}
	def getStems(self):
		return {w:self for w in self.getBareStems()}
	def getBareStems(self):
		return self.json['stemmed'] if 'stemmed' in self.json.keys() else {}
	def getQTags(self):
		return self.tags if self.tags else []
