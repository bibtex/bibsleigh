#!/usr/local/bin/python3

from template import bibHTML
import xml.etree.cElementTree as ET

locations = []

numfixes = {
	'1st': 'First',
	'2nd': 'Second',
	'3rd': 'Third',
	'4th': 'Fourth',
	'5th': 'Fifth',
	'6th': 'Sixth',
	'7th': 'Seventh',
	'8th': 'Eighth',
	'9th': 'Ninth',
	'10th': 'Tenth',
	'Eleventh': '11th',
	'Twelfth': '12th'
}

class BibLib(object):
	def __init__(self):
		self.xs = []
	def __iadd__(self,other):
		b = BibEntry()
		b.loadXMLe(other)
		b.sanitize()
		self.xs.append(b)
		print('Added:', b.key)
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
	def toBIB(self):
		s = '@%s{%s,\n' % (self.t, self['key'][0])
		for k in self.args:
			if k in ('author', 'editor'):
				s += '\t%-10s = "%s",\n' % (k,' and '.join(self.dict[k]))
			elif k in ('title', 'booktitle'):
				if len(self.dict[k])==1:
					s += '\t%-10s = "{%s}",\n' % (k,self.dict[k][0])
				else:
					s += '\t%-10s = "{%s (%s)}",\n' % (k,self.dict[k][0],self.dict[k][1])
			elif k in ('ee','crossref','key'):
				pass
			elif k == 'doi':
				s += '\t%-10s = "<a href="http://dx.doi.org/%s">%s</a>",\n' % (k,self.dict[k][0],self.dict[k][0])
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
		if not self['url'][0].startswith('http://'):
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
		self['key'] = self['booktitle'][0].upper()+'-'+tmp+self['year'][0]
		# fix title for conferences
		if self['title'][0].count(',')>2 and self['title'][0].find('Conference')>0:
			cs = self['title'][0].split(', ')
			ds = []
			title = ''
			for c in cs:
				if c.isdigit():
					continue
				if self['booktitle'] and c.startswith(self['booktitle'][0]) and c.replace(self['booktitle'][0],'').strip().isdigit():
					continue
				if c.startswith('January') or c.startswith('February') or c.startswith('March') or c.startswith('April') or c.startswith('May') or c.startswith('June') or c.startswith('July') or c.startswith('August') or c.startswith('September') or c.startswith('October') or c.startswith('November') or c.startswith('December'):
					continue
				if c in locations:
					continue
				if c.find('Conference')>-1:
					title = c
					continue
				ds.append(c)
			ds[0] = '%s on %s' % (title, ds[0])
			if len(ds)==2:
				self.dict['title'] = ['%s of the %s' % (ds[1],ds[0])]
			else:	
				self.dict['title'] = [', '.join(ds)]
			for k in numfixes:
				self.dict['title'][0] = self.dict['title'][0].replace(k,numfixes[k])
			print('Still got:',ds)
	def prioritise(self, arg):
		if arg in self.args:
			self.args.remove(arg)
			self.args = [arg] + self.args
		else:
			# print('Warning: no %s defined!' % arg)
			pass
	def updatewith(self, xref):
		print('Updating',self.key,'with',xref.key)
		for inh in ('editor','publisher','isbn','volume','series'):
			for v in xref[inh]:
				self[inh] = v
		self.dict['booktitle'] = [xref.dict['title'][0],xref.dict['booktitle'][0]]
		pass
	def writeHTML(self,fs):
		h = open(fs,'w',encoding='utf-8')
		h.write(bibHTML %
			(self.getTitleTXT(),
			self.getAuthorsHTML(),
			self.getTitleHTML(),
			self.getVenueHTML(),
			self.toBIB()))
		h.close()
	def getAuthorsHTML(self):
		if self['author']:
			return ', '.join(self['author'])
		else:
			return ', '.join(self['editor'])+' (editors)'
	def getTitleTXT(self):
		# TODO: not exhaustive
		return self['title'][0].replace('<i>','').replace('</i>','')
	def getTitleHTML(self):
		return self['title'][0]
	def getVenueHTML(self):
		return '%s, %s' % (self['booktitle'][0], self['year'][0])


if __name__ == '__main__':
	f = open('locations.lst','r')
	locations = f.read().split('\n')
	f.close()
	xs = BibLib()
	# parser = ET.XMLParser(encoding="ISO-8859-1")
	parser = ET.XMLParser(encoding="utf-8")
	# for event, elem in ET.iterparse('dblp.xml', events=("end",)):
	for event, elem in ET.iterparse('try.xml', events=("end",), parser=parser):
		# If the 'events' option is omitted, only “end” events are returned.
		if elem.findtext('booktitle')=='SLE':
			xs += elem
			elem.clear()
	for x in xs:
		print('I got', x.key)
		if x['crossref'] and xs[x['crossref'][0]]:
			x.updatewith(xs[x['crossref'][0]])
	xs.writeHTML()
