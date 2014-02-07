#!/usr/local/bin/python3

import xml.etree.cElementTree as ET

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
				s += '\t%-10s = "{%s}",\n' % (k,self.dict[k][0])
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
		pass
	def writeHTML(self,fs):
		h = open(fs,'w')
		h.write('''<?xml version="1.0" encoding="UTF-8"?>
		<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
		<html xmlns="http://www.w3.org/1999/xhtml" xmlns:xhtml="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
		<head>
			<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
			<meta name="keywords" content="software linguistics, software language engineering, book of knowledge, glossary, Russian; иньекция; English; inject"/>
			<title>SL(E)BOK — bibSLEIGH — %s</title>
			<link href="../sleg.css" rel="stylesheet" type="text/css"/>
		</head>
		<body>
		<div class="left">
			(a link to bibSLEIGH)<br/>
			<a href="index.html"><img src="../conf/sle.png" alt="Software Language Engineering" class="pad"/></a><br/>
			(a link to edit)<br/>
			<a href="http://creativecommons.org/licenses/by-sa/3.0/" title="CC-BY-SA"><img src="../www/cc-by-sa.png" alt="CC-BY-SA"/></a><br/>
			<a href="http://creativecommons.org/licenses/by-sa/3.0/" title="Open Knowledge"><img src="../www/open-knowledge.png" alt="Open Knowledge" class="pad" /></a><br/>
			<a href="http://validator.w3.org/check/referer" title="XHTML 1.0 W3C Rec"><img src="../www/xhtml10.png" alt="XHTML 1.0 W3C Rec" /></a><br/>
			<a href="http://jigsaw.w3.org/css-validator/check/referer" title="CSS 2.1 W3C CanRec"><img src="../www/css21.png" alt="CSS 2.1 W3C CanRec" class="pad" /></a><br/>
			<div>[<a href="mailto:vadim@grammarware.net">Complain!</a>]</div>
		</div>
		<div class="main">
		<h2>
			%s<br/>
			<em>%s</em>.<br/>
			%s.
		</h2>
		<pre>%s</pre>
		<div style="clear:both"/><hr />
		<div class="last">
			<em>
				<a href="http://github.com/slebok/bibsleigh">Bibliography of Software Language Engineering IGH</a> (BibSLEIGH) is
				created and maintained by <a href="http://grammarware.net">Dr. Vadim Zaytsev</a>.<br/>
				Hosted as a part of <a href="http://slebok.github.io/">SLEBOK</a> on <a href="http://www.github.com/">GitHub</a>.
			</em>
		</div></body></html>''' %
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
	xs = BibLib()
	# for event, elem in ET.iterparse('dblp.xml', events=("end",)):
	for event, elem in ET.iterparse('try.xml', events=("end",)):
		# If the 'events' option is omitted, only “end” events are returned.
		if elem.findtext('booktitle')=='SLE':
			xs += elem
			elem.clear()
	for x in xs:
		print('I got', x.key)
		if x['crossref'] and xs[x['crossref'][0]]:
			x.updatewith(xs[x['crossref'][0]])
	xs.writeHTML()
	