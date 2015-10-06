#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for natural language processing

trash = ('-', \
	'a', 'an', 'and', 'as', 'at', \
	'by', \
	'for', 'from', \
	'how', \
	'in', \
	'of', 'on', \
	's', \
	'the', 'through', 'to', 'towards', \
	'via', \
	'with')

nrs = {'1st': 'First', '2nd': 'Second', '3rd': 'Third', '1th': 'First', '2th': 'Second', \
'3th': 'Third', '4th': 'Fourth', '5th': 'Fifth', '6th': 'Sixth', '7th': 'Seventh', \
'8th': 'Eighth', '9th': 'Ninth', 'Tenth': '10th', 'Eleventh': '11th', 'Twelfth': '12th', \
'Thirteenth': '13th', 'Fourteenth': '14th', 'Fifteenth': '15th', 'Sixteenth': '16th', \
'Seventeenth': '17th', 'Eighteenth': '18th', 'Nineteenth': '19th', 'Twentieth': '20th'}

def strictstrip(s):
	s = s.strip()
	if s.endswith(','):
		s = s[:-1]
	return s

def shorten(n):
	ws = n.split(' ')
	if len(ws) == 1:
		return n
	return '.'.join([w[0] for w in ws[:-1]]) + '.' + ws[-1]

def baretext(s):
	s = s.strip().lower()
	for tag in ('i', 'sub', 'sup'):
		s = s.replace('<'+tag+'>', '')
		s = s.replace('</'+tag+'>', '')
	return s

def superbaretext(s):
	for x in '},.:!?;./\\“”‘’–—_=@$%^&()[]§±`~<>|\'#+1234567890{':
		s = s.replace(x, ' ')
	while s.find('  ') > -1:
		s = s.replace('  ', ' ')
	return s.strip()

def heurichoose(k, v1, v2):
	if k == 'title':
		# title without spaces if bad
		if v1.find(' ') < 0 and v2.find(' ') >= 0:
			return v2
		if v2.find(' ') < 0 and v1.find(' ') >= 0:
			return v1
		# proceedings are always good
		if v1.startswith('Proceedings') and not v2.startswith('Proceedings'):
			return v1
		if v2.startswith('Proceedings') and not v1.startswith('Proceedings'):
			return v2
		if v1.startswith('Proceedings') and v2.startswith('Proceedings'):
			if v1.count(',') > v2.count(','):
				return v2
			else:
				return v1
	if k == 'year':
		# updated year always gets precedence
		return v1
	# print('{}: {} vs {}'.format(C.red('\tUndecided ' + k), v1, v2))
	# if undecided, stick to the old one
	return v2
