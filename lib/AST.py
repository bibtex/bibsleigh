#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module with classes forming the abstract syntax of BibSLEIGH

import glob, os.path
from fancy.Templates import uberHTML, confHTML, bibHTML
from lib.JSON import jsonkv, parseJSON
from lib.LP import listify

def escape(s):
	for k, v in ((' ', '%20'), ('+', '%2B'), ('#', '%23')):
		s = s.replace(k, v)
	return s

# Sort first by year, then by pages
def sortbypages(z):
	p1, _ = z.getPagesTuple()
	y = z.get('year')
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
		for k in sorted(self.json.keys()):
			if k == k.upper() or k.endswith('short') or k == 'tag':
				# secret key
				continue
			if k in ('author', 'editor'):
				s += '\t{:<10} = "{}",\n'.format(k, ' and '.join(listify(self.json[k])))
			elif k in ('title', 'booktitle', 'series', 'publisher', 'journal'):
				if k+'short' not in self.json.keys():
					s += '\t{0:<10} = "{{{1}}}",\n'.format(k, self.json[k])
				else:
					s += '\t{0:<10} = "{{<span id="{0}">{1}</span>}}",\n'.format(k, self.json[k])
			elif k in ('crossref', 'key', 'type', 'venue', 'twitter', \
				'eventtitle', 'eventurl', 'nondblpkey', 'dblpkey', 'dblpurl', \
				'programchair', 'generalchair'):
				# TODO: ban 'ee' as well
				pass
			elif k == 'doi':
				s += '<span class="uri">\t{0:<10} = "<a href="http://dx.doi.org/{1}">{1}</a>",\n</span>'.format(k, self.json[k])
			elif k == 'acmid':
				s += '<span class="uri">\t{0:<10} = "<a href="http://dl.acm.org/citation.cfm?id={1}">{1}</a>",\n</span>'.format(k, self.json[k])
			elif k == 'dblpkey':
				# Legacy!
				# s += '\t{0:<10} = "<a href="http://dblp.uni-trier.de/db/{1}">{1}</a>",\n</span>'.format(k, self.json[k])
				s += '\t{0:<10} = "<a href="http://dblp.uni-trier.de/rec/html/{1}">{1}</a>",\n'.format(k, self.json[k])
			elif k == 'isbn':
				s += '<span id="isbn">\t{:<10} = "{}",\n</span>'.format(k, self.json[k])
			elif k in ('ee', 'url'):
				for e in listify(self.json[k]):
					# VVZ: eventually would like to get rid of EE completely
					# VVZ: limiting it for now to possibly interesting cases
					if k == 'ee' and (e.startswith('http://dx.doi.org') or \
						e.startswith('http://dl.acm.org') or\
						e.startswith('http://doi.ieeecomputersociety.org')\
					):
						continue
					s += '<span class="uri">\t{0:<10} = "<a href=\"{1}\">{1}</a>",\n</span>'.format(k, e)
			elif k in ('year', 'volume', 'issue', 'number') and isinstance(self.json[k], int):
				s += '\t{0:<10} = {1},\n'.format(k, self.json[k])
			elif k == 'pages':
				s += '\t{0:<10} = "{1}",\n'.format(k, self.getPagesBib())
			else:
				s += '\t{0:<10} = "{1}",\n'.format(k, self.json[k])
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
		if 'dblpkey' in self.json.keys():
			links[1].append('<a href="http://dblp.uni-trier.de/rec/html/{}">DBLP</a>'.format(\
				self.json['dblpkey']))
		elif 'dblpurl' in self.json.keys():
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
				if e.find('dl.acm.org') > 0 or e.find('doi.acm.org') > 0:
					links[2].append('<a href="{}">ACM DL</a>'.format(e))
				elif e.find('ieeexplore.ieee.org') > 0:
					links[2].append('<a href="{}">IEEE Xplore</a>'.format(e))
				elif e.find('ieeecomputersociety.org') > 0:
					links[2].append('<a href="{}">IEEE CS</a>'.format(e))
				elif e.find('dagstuhl.de') > 0:
					links[2].append('<a href="{}">Dagstuhl</a>'.format(e))
				elif e.find('computer.org/csdl/proceedings') > 0:
					links[2].append('<a href="{}">CSDL</a>'.format(e))
				elif e.find('dx.doi.org') > 0:
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
			ps = self.json['pages'].split('-')
			if ps[0]:
				if ':' in ps[0]:
					p1 = int(ps[0].split(':')[-1].strip())
				else:
					p1 = int(ps[0])
			else:
				p1 = None
			if ps[-1]:
				p2 = int(ps[-1])
			else:
				p2 = None
		return (p1, p2)

class Sleigh(Unser):
	def __init__(self, idir):
		super(Sleigh, self).__init__('', idir)
		self.venues = []
		for d in glob.glob(idir+'/*'):
			if d.endswith('.md'):
				continue
			self.venues.append(Venue(d, idir, self))
	def getPage(self):
		return uberHTML.format(\
			len(self.venues),
			self.numOfPapers(),
			self.numOfVolumes(),
			'\n'.join([v.getItem() for v in self.venues]))
	def seek(self, key):
		f = None
		for v in self.venues:
			f = v.seek(key)
			if f:
				return f
		return f
	def seekByKey(self, key):
		f = None
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


class Venue(Unser):
	def __init__(self, d, hdir, parent):
		super(Venue, self).__init__(d, hdir)
		self.years = []
		for f in glob.glob(d+'/*'):
			if f.endswith('.json'):
				self.json = parseJSON(f)
			elif os.path.isdir(f):
				self.years.append(Year(f, self.homedir, self))
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
		# TO-DO: check if img exists
		return ('<div class="picx"><a href="{ABBR}.html" title="{title}">'+\
			'<img src="stuff/{abbr}.png" alt="{title}"/><h2>{ABBR}</h2></a></div>').format(\
				ABBR=ABBR,\
				abbr=ABBR.lower(),\
				title=title)
	def getPage(self):
		if 'eventurl' in self.json.keys():
			if 'twitter' in self.json.keys():
				ev = '<h3>Event series page: <a href="{uri}">{uri}</a> (<a href="https://twitter.com/{twi}">@{twi}</a>)</h3>'.format(uri=self.json['eventurl'], twi=self.json['twitter'])
			else:
				ev = '<h3>Event series page: <a href="{uri}">{uri}</a></h3>'.format(uri=self.json['eventurl'])
		else:
			ev = ''
		ABBR = self.get('name')
		title = self.get('title')
		img = ABBR.lower()
		eds = [y.getItem() for y in sorted(self.years, reverse=True, key=lambda x: x.year)]
		return confHTML.format(\
			filename='{0}/{0}.json'.format(self.getPureName()),\
			title=ABBR,\
			img=img,\
			fname=('{} ({})'.format(title, ABBR)),\
			venpage=ev,\
			dl=''.join(eds))
	def getConfs(self):
		res = []
		for y in self.years:
			res.extend(y.confs)
		return res
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
		for y in self.years:
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


class Year(Unser):
	def __init__(self, d, hdir, parent):
		super(Year, self).__init__(d, hdir)
		self.year = last(d)
		self.confs = []
		jsonsfound = []
		jsonsused = []
		for f in glob.glob(d+'/*'):
			if os.path.isdir(f):
				self.confs.append(Conf(f, self.homedir, self))
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
				self.confs.append(Conf(f[:f.rindex('.')], self.homedir, self))
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
	def __init__(self, d, hdir, parent):
		super(Conf, self).__init__(d, hdir)
		self.papers = []
		self.year = parent.year
		for f in glob.glob(d+'/*'):
			if os.path.isfile(f) and f.endswith('.json'):
				self.papers.append(Paper(f, self.homedir, self))
			else:
				print('File or directory out of place:', f)
		self.back = parent
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
		if 'eventurl' in self.json.keys():
			if 'twitter' in self.json.keys():
				ev = '<h3>Event page: <a href="{uri}">{uri}</a> (<a href="https://twitter.com/{twi}">@{twi}</a>)</h3>'.format(uri=self.json['eventurl'], twi=self.json['twitter'])
			else:
				ev = '<h3>Event page: <a href="{uri}">{uri}</a></h3>'.format(uri=self.json['eventurl'])
		else:
			ev = ''
		if 'generalchair' in self.json.keys() or 'programchair' in self.json.keys():
			positions = [(c, 'General Chair') for c in listify(self.json['generalchair'])] \
			          + [(c, 'Program Chair') for c in listify(self.json['programchair'])]
			ev += '<h3>Committee: ' + ', '.join(['<a href="person/{}.html">{}</a> ({})'.format(\
				c.replace(' ', '_'),
				c,t) for c,t in positions]) + '</h3>'
		return bibHTML.format(\
			filename=self.getJsonName(),
			title=self.get('title'),
			img=self.get('venue').lower(), # geticon?
			authors=self.getAuthors(),
			short='{}, {}'.format(self.get('booktitle'), self.get('year')),
			code=self.getCode(),
			bib=self.getBib(),
			boxlinks=self.getBoxLinks(),
			contents=ev+'<h3>Contents ({} items)</h3><dl class="toc">'.format(len(self.papers))+\
				'\n'.join([p.getItem() for p in sorted(self.papers, key=sortbypages)])+'</dl>'\
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
	def getItemWTags(self, tgz):
		return '<dt><a href="{0}.html">{0}</a>{4}</dt><dd>{1}{2}{3}.</dd>'.format(\
			self.getKey(),\
			self.get('title').replace('&', '&amp;'),\
			self.getAbbrAuthors(),\
			self.getPagesString(),
			tgz)
	def getItem(self):
		return self.getItemWTags(self.getFancyTags(self.tags) if self.tags else '')
	def getRestrictedItem(self, t):
		if not self.tags:
			return self.getItemWTags('')
		else:
			ts = self.tags[:]
			if t in ts:
				ts.remove(t)
			return self.getItemWTags(self.getFancyTags(ts))
	def getFancyTags(self, ts):
		# TODO: do the same backlinks for bundles
		return ' ' + ' '.join(['<span class="tag"><a href="tag/{}.html" title="{}">&nbsp;T&nbsp;</a></span>'.format(escape(t), t) for t in ts])
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
			cnt += '\n'.join(['<li><a href="tag/{}.html">{}</a></li>'.format(escape(t), t) for t in self.tags])
			cnt += '</ul><hr/>'
		else:
			cnt = ''
		return bibHTML.format(\
			filename=self.getJsonName(),
			title=self.get('title'),
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
		if self.tags:
			# myname = self.getHtmlName()
			return {k:self for k in self.tags}
		else:
			return {}
