#!/usr/local/bin/python3

import xml.etree.cElementTree as ET
# import elementtree.ElementTree as ET
# import urllib, urllib2, httplib, socket

# def safelyLoadURL(url):
# 	print('(loading %s...)' % url)
# 	errors = 0
# 	while errors<3:
# 		try:
# 			return urllib.urlopen(url).read()
# 		except IOError:
# 	 		print( 'Warning: failed to load URL, retrying...')
# 	 		errors += 1
# 		except socket.error:
# 			print( 'Warning: connection reset by peer, retrying...')
# 			errors += 1
# 	print( 'Error fetching URL:',url)
# 	return ''


class BibEntry(object):
	def __init__(self):
		self.dict = {}
		self.args = []
		self.t = ''
		self.key = ''
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
			self.dict[e.tag] = e.text
			self.args.append(e.tag)
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
		s = '@%s{%s,\n' % (self.t, self.key)
		for k in self.args:
			s += '\t%s = "%s",\n' % (k,self.dict[k])
		return s+'}'
	def sanitize(self):
		for k in self.dict.keys():
			# make all pairs observable
			if k not in self.args:
				self.args.append(k)
			# remove tailing dots
			if type(self.dict[k]) == type(''):
				self.dict[k] = self.dict[k].strip()
				if self.dict[k].endswith('.'):
					self.dict[k] = self.dict[k][:-1]
			else:
				print(self.dict)
		# turn ee into doi
		# <ee>http://dx.doi.org/10.1007/978-3-540-87875-9_2</ee>
		if 'ee' in self.args and 'doi' not in self.args and self.dict['ee'].startswith('http://dx.doi.org/'):
			self.args.append('doi')
			self.dict['doi'] = self.dict['ee'].split('http://dx.doi.org/')[-1]


if __name__ == '__main__':
	xs = []
	for event, elem in ET.iterparse('dblp.xml', events=("end",)):
		# If the 'events' option is omitted, only “end” events are returned.
		if elem.tag == 'inproceedings' and elem.findtext('booktitle')=='SLE':
			b = BibEntry()
			b.loadXMLe(elem)
			b.sanitize()
			xs.append(b)
			elem.clear()
			print( 'YES!' + b.key)
		# print( elem.tag)
		pass
