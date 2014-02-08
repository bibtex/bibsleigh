#!/usr/local/bin/python3

from template import bibHTML, confHTML, uberHTML
from venues import venuesMap
from short import contractions
from supported import supported
import xml.etree.cElementTree as ET

unk = []

locations = []

def purenum(a):
	num = int(''.join([x for x in a if x.isdigit()]))
	if num < 10:
		return '200%s' % num
	elif num < 40:
		return '20%s' % num
	elif num < 100:
		return '19%s' % num
	else:
		return str(num)

class BibLib(object):
	def __init__(self):
		self.xs = []
	def __iadd__(self,other):
		b = BibEntry()
		b.loadXMLe(other)
		b.sanitize()
		self.xs.append(b)
		print('Added:', b.key)
		other.clear()
		return self
	def __getitem__(self,key):
		for x in self.xs:
			if x.key == key:
				return x
		return None
	def __len__(self):
		return len(self.xs)
	def __iter__(self):
		return self.xs.__iter__()
	def writeHTML(self):
		for x in self.xs:
			fn = 'html/%s.html' % x['key'][0]
			x.writeHTML(fn)

class BibEntry(object):
	def __init__(self):
		self.dict = {}
		self.args = []
		self.t = ''
		self.key = ''
		self.linked = []
	def __getitem__(self,key):
		if key in self.args:
			return self.dict[key]
		else:
			return None
	def __setitem__(self,key,val):
		# NB: assignment works as appending!
		if key in self.args:
			self.dict[key].append(val)
		else:
			self.args.append(key)
			self.dict[key] = [val]
	def loadBIB(self, fs):
		f = open(fs,'r')

		f.close()
	def loadXML(self, fs):
		self.loadXMLe(ET.parse(fs).findall('*')[0])
	def loadXMLe(self, x):
		self.t = x.tag
		self.key = x.attrib['key']
		for e in x.findall('*'):
			# print '%s = "%s",' % (e.tag, e.text)
			if e.tag not in self.args:
				self.args.append(e.tag)
				self.dict[e.tag] = []
			newval = e.text
			# newval = ET.tostring(e,encoding="ISO-8859-1")
			if not e.text:
				newval = ''
			# NB: only works on one level of mixed content nesting
			for subel in e[:]:
				if subel.tail:
					tail = subel.tail
				else:
					tail = ''
				newval += '<%s>%s</%s>%s' % (subel.tag,subel.text,subel.tag,tail)
			self.dict[e.tag].append(newval)
	def unloadXML(self,fs):
		f = open(fs,'w')
		f.write(self.toXML())
		f.close()
	def toXML(self):
		s = '<?xml version="1.0"?>\n<dblp>\n<%s key="%s">\n' % (self.t, self.key)
		for k in self.args:
			s += '<%s>%s</%s>\n' % (k,self.dict[k],k)
		return s+'</%s>\n</dblp>\n' % self.t
	def unloadBIB(self,fs):
		f = open(fs,'w')
		f.write(self.toBIB())
		f.close()
	def getKeyHTML(self):
		if self['booktitle'] and self['year']:
			es = self['key'][0].split('-')
			if len(es)==3 and es[2].isdigit() and es[0]==self['booktitle'][-1]:
				# we are a paper => refer to the corresponding conference edition
				return '<a href="%s-%s.html">%s</a>-%s-%s' % (es[0],es[2],es[0],es[1],es[2])
			if len(es)==2 and es[1].isdigit() and es[0]==self['booktitle'][-1]:
				# we are a conference edition => refer to the series
				return '<a href="%s.html">%s</a>-%s' % (es[0],es[0],es[1])
		return self['key'][0]
	def toBIB(self):
		s = '@%s{%s,\n' % (self.t, self.getKeyHTML())
		for k in self.args:
			if k in ('author', 'editor'):
				s += '\t%-10s = "%s",\n' % (k,' and '.join(self.dict[k]))
			elif k in ('title', 'booktitle', 'series', 'publisher'):
				if len(self.dict[k])==1:
					s += '\t%-10s = "{%s}",\n' % (k,self.dict[k][0])
				else:
					s += '\t%-10s = "{<span id="%s">%s</span>}",\n' % (k,k,self.dict[k][0])
			elif k in ('ee','crossref','key'):
				pass
			elif k == 'doi':
				s += '\t%-10s = "<a href="http://dx.doi.org/%s">%s</a>",\n' % (k,self.dict[k][0],self.dict[k][0])
			elif k == 'isbn':
				s += '<span id="isbn">\t%-10s = "%s",\n</span>' % (k,self.dict[k][0])
			else:
				s += '\t%-10s = "%s",\n' % (k,self.dict[k][0])
		s += '}'
		return s.replace('<i>','\\emph{').replace('</i>','}')
	def sanitize(self):
		for k in self.dict.keys():
			# make all pairs observable
			if k not in self.args:
				self.args.append(k)
			# remove tailing dots
			if type(self.dict[k]) != type([]):
				print('Not a list:',self.dict[k])
				self.dict[k] = []
			for i in range(0,len(self.dict[k])):
				if type(self.dict[k][i]) == type(''):
					self.dict[k][i] = self.dict[k][i].strip()
					if self.dict[k][i].endswith('.'):
						self.dict[k][i] = self.dict[k][i][:-1]
				else:
					print('Something wrong here:',self.dict)
		# turn ee into doi
		# <ee>http://dx.doi.org/10.1007/978-3-540-87875-9_2</ee>
		if 'ee' in self.args and 'doi' not in self.args and self.dict['ee'][0].startswith('http://dx.doi.org/'):
			self['doi'] = self.dict['ee'][0].split('http://dx.doi.org/')[-1]
		# fix title: capitalise
		# TODO
		# fix pages:
		ps = self['pages']
		if not ps:
			print('Warning: no pages defined!')
		else:
			self.dict['pages'] = [ps[0].split('-')[0]+'--'+ps[0].split('-')[-1]]
		# fix order: author, title, venue, year, rest
		for x in ('editor','year','booktitle','title','author'):
			self.prioritise(x)
		# fix url: drop if local
		if self['url'] and not self['url'][0].startswith('http://'):
			self.args.remove('url')
			self.dict.pop('url')
		# fix key:
		tmp = self.key.split('/')[-1]
		if tmp[-4:].isdigit():
			tmp = tmp[:-4]
		elif tmp[-2:].isdigit():
			tmp = tmp[:-2]
		if tmp:
			tmp += '-'
		# NB: self['year'] can be incorrect (e.g., SLE used to publish proceedings the year after the event)
		self['key'] = self['booktitle'][0].upper()+'-'+tmp+purenum(self.key)
		# fix title for conferences
		if self['title'][0] in venuesMap.keys():
			self.dict['title'] = [venuesMap[self['title'][0]]]
		# fix series
		for ctr in ('series','publisher'):
			if self[ctr] and len(self[ctr])==1:
				for a in contractions:
					if self[ctr][0] == a[0]:
						self.dict[ctr] = a
	def prioritise(self, arg):
		if arg in self.args:
			self.args.remove(arg)
			self.args = [arg] + self.args
		else:
			# print('Warning: no %s defined!' % arg)
			pass
	def updatewith(self, xref):
		xref.linked.append(self)
		print('Updating',self.key,'with',xref.key)
		for inh in ('editor','publisher','isbn','volume','series'):
			if xref[inh]:
				for v in xref[inh]:
					self[inh] = v
		self.dict['booktitle'] = [xref.dict['title'][0],xref.dict['booktitle'][0]]
		self.sanitize()
	def writeHTML(self,fs):
		h = open(fs,'w',encoding='utf-8')
		h.write(bibHTML %
			(self.getTitleTXT(),
			self.getVenueIcon(),
			self.getVenueShort(),
			self.getVenueShort(),
			self.getAuthorsHTML(),
			self.getTitleHTML(),
			self.getVenueHTML(),
			self.getCodeLongShort(),
			self.toBIB(),
			self.contentsHTML()))
		h.close()
	def getVenueShort(self):
		if self['booktitle'] and self['booktitle'][-1] in supported.keys():
			return supported[self['booktitle'][-1]]
		else:
			return self.getVenueHTML()
	def contentsHTML(self):
		if not self.linked:
			return ''
		items = {}
		for link in self.linked:
			if link['pages']:
				p = int(link['pages'][0].split('-')[0])
				pp = ', pp. ' + link['pages'][0].replace('--','–')
			else:
				p = 0
				pp = ''
				while p in items.keys():
					p -= 1
			items[p] = '<dt><a href="%s.html">%s</a></dt><dd>%s (%s)%s.</dd>' % (link['key'][0], link['key'][0], link.getTitleHTML(), link.getAuthorsShortHTML(), pp)
		return ('<h3>Contents (%s items)</h3><dl class="toc">' % len(items))+ ''.join([items[i] for i in sorted(items.keys())]) + '</dl>'
	def getAuthorsShortHTML(self):
		if not self['author']:
			return '—'
		return ', '.join(['<abbr title="%s">%s</abbr>' % (name,''.join([s[0] for s in name.split(' ') if s[0].isalpha()])) for name in self['author']])
	def getAuthorsHTML(self):
		if self['author']:
			return ', '.join(self['author'])
		elif self['editor']:
			return ', '.join(self['editor'])+' (editors)'
		else:
			print('ERROR: neither authors nor editor in',self.key)
			return ''
	def getTitleTXT(self):
		# TODO: not exhaustive
		return self['title'][0].replace('<i>','').replace('</i>','')
	def getTitleHTML(self):
		return self['title'][0]
	def getVenueIcon(self):
		return self['booktitle'][-1].lower()
	def getVenueHTML(self):
		return '%s, %s' % (self['booktitle'][0], self['year'][0])
	def getCodeLongShort(self):
		code = ''
		for tag in ('title','booktitle','series','publisher'):
			if self[tag] and len(self[tag])==2:
				code += "$('#"+tag+"').text(this.checked?'%s':'%s');" % tuple(self[tag])
		return code


if __name__ == '__main__':
	f = open('locations.lst','r')
	locations = f.read().split('\n')
	f.close()
	xs = BibLib()
	parser = ET.XMLParser(encoding="utf-8")
	# for event, elem in ET.iterparse('try.xml', events=("end",), parser=parser):
	for event, elem in ET.iterparse('dblp.xml', events=("end",), parser=parser):
		# If the 'events' option is omitted, only “end” events are returned.
		if elem.findtext('booktitle') in supported.keys():
			xs += elem
	for x in xs:
		print('I got', x.key)
		if x['crossref'] and xs[x['crossref'][0]]:
			x.updatewith(xs[x['crossref'][0]])
			unk.append(xs[x['crossref'][0]]['title'][0])
	xs.writeHTML()
	print(len(xs),'bib entries processed.')
	un = []
	for x in unk:
		if x not in venuesMap.keys() and x not in venuesMap.values():
			un.append(x)
	print(len(un),'unknown venue names.')
	f = open('venues.lst','w')
	f.write('\n'.join(un))
	f.close()
	confs = []
	for ven in supported.keys():
		f = open('html/%s.html' % ven, 'w')
		# f.write(ConfHTML % (supported[ven],))
		f.write(confHTML %
			(supported[ven],
			ven.lower(),
			supported[ven],
			supported[ven],
			'%s (%s)' % (supported[ven],ven),
			''))
		f.close()
		confs.append('<div class="pic"><a href="%s.html" title="%s"><img src="../conf/%s.png" alt="%s"><br/>%s</a></div>' %
			(ven,
			supported[ven],
			ven.lower(),
			supported[ven],
			ven
			))
	print(len(supported),'venues.')
	f = open('html/index.html','w')
	f.write(uberHTML % '\n'.join(sorted(confs)))
	f.close()
