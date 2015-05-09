#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import glob, os.path

# SANER (icon, venue page)
# 	2012 (section on the venue page)
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

class Venue(object):
	# def __init__(self, args):
	# 	self.years = args
	# 	self.json = {}
	def __init__(self, d):
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

class Year(object):
	def __init__(self, d):
		self.year = last(d)
		self.confs = []
		for f in glob.glob(d+'/*'):
			if os.path.isdir(f):
				self.confs.append(Conf(f))
			else:
				print('File out of place:', f)
	def numOfPapers(self):
		return sum([c.numOfPapers() for c in self.confs])

class Conf(object):
	def __init__(self, d):
		self.papers = []
		for f in glob.glob(d+'/*'):
			if os.path.isfile(f) and f.endswith('.json'):
				self.papers.append(Paper(f))
			else:
				print('File or directory out of place:', f)
	def numOfPapers(self):
		return len(self.papers)

class Paper(object):
	def __init__(self, f):
		self.json = parseJSON(f)
