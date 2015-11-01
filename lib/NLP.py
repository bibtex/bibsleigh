#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for natural language processing

import re

trash = ('-', \
	'and', 'are', \
	'for', 'from', \
	'her', 'hers', 'him', 'his', 'how', \
	'its', 'into', \
	'over', \
	'she', \
	'the', 'they', 'them', 'their', 'through', \
	'via', \
	'with', \
	'you', 'your', 'yours' \
	)
# 19210 stems found.

nosplit = (\
	'JastAdd', \
	'JavaScript', \
	'MontiCore', \
	)

nofilter = (\
	'ad', \
	'be', \
	'do', \
	'go', \
	'id', \
	'ml', \
	'no', \
	'tv', \
	'ui', \
	'up', \
	)

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
	# print('SHORTEN[{}]'.format(n))
	ws = n.strip().split(' ')
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

# Works almost like .split() but much stricter:
# 	- saves only proper letters
# 	- treats any other symbol as a words separator
# 	- converts words to lower case
#	- tries to break CamelCase, CamelTAIL and HEADCamel (no CamelMIDCase)
# 	- resists the temptation to treat ABBRs as HEADCamel
def string2words(s):
	ws = ['']
	for c in s:
		if c.isalpha():
			ws[-1] += c
		elif ws[-1] != '':
			ws.append('')
	if ws[-1] == '':
		ws = ws[:-1]
	ws2 = []
	for w in ws:
		if w[-1] == 's' and w[:-1].isupper():
			# corner case: DAGs, NDAs, APIs, etc
			ws2.append(w)
			continue
		if re.match('^[A-Z]+to[A-Z]+', w):
			# corner case: XXXtoYYY
			uc = re.findall('[A-Z]+', w)
			ws2.append(uc[0])
			ws2.append('to')
			ws2.append(uc[1])
			continue
		ccws = re.findall('[A-Z][a-z]+', w)
		recon = ''.join(ccws)
		if w not in nosplit and len(ccws) > 1 and recon == w:
			# primary case: a word cleanly split into words
			# print('[  CC  ]', w, '->', ' ++ '.join(ccws))
			ws2.extend(ccws)
		elif w.endswith(recon) and re.match('^[A-Z]+$', w[:-len(recon)]):
			# corner case: starts with an abbreviation, continues to camel
			# print('[  CC  ]', w, '->', w[:-len(recon)], '±±', ' ++ '.join(ccws))
			ws2.append(w[:-len(recon)])
			ws2.extend(ccws)
		elif w.startswith(recon) and re.match('^[A-Z]+$', w[len(recon):]):
			# corner case: starts with a camel, ends with an abbreviation
			# print('[  CC  ]', w, '->', ' ++ '.join(ccws), '±±', w[len(recon):])
			ws2.extend(ccws)
			ws2.append(w[len(recon):])
		else:
			ws2.append(w)
	return [w.lower() for w in ws2] # if w.lower() not in trash or w.lower() in nofilter]

def ifIgnored(w):
	return not ifApproved(w)

def ifApproved(w):
	return w in nofilter or (w not in trash and len(w) > 2)
