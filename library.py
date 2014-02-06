#!/usr/bin/python

import elementtree.ElementTree as ET

class BibEntry(object):
	"""docstring for BibEntry"""
	def __init__(self):
		self.dict = {}
		self.args = []
		self.t = ''
		self.key = ''
	def loadBIB(self, fs):
		f = open(fs,'r')

		f.close()
	def loadXML(self, fs):
		x = ET.parse(fs)
		self.t = x.findall('*')[0].tag
		self.key = x.findall('*')[0].attrib['key']
		for e in x.findall('*')[0].findall('*'):
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


if __name__ == '__main__':
	b = BibEntry()
	b.loadXML('Diskin08.xml')
	b.unloadXML('Diskin08_.xml')
