#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import sys, os

def js(s):
	if len(s) == 1:
		return '"{}"'.format(s[0])
	else:
		return '[' + ', '.join(['"{}"'.format(b) for b in s]) + ']'

def deentitify(z):
	return z.replace('ü', 'ue').replace('ä', 'ae')

f = open(sys.argv[1])
keystart = sys.argv[1].split('.')[0].upper()
lines = f.readlines()
f.close()
i = 0
cx = 0
d = {}
used = []
if not os.path.exists(keystart):
	os.makedirs(keystart)
	print('[ √ ] Directory', keystart, 'created.')
while i < len(lines):
	while lines[i].startswith('@'):
		k = lines[i][1:lines[i].index(': ')]
		v = lines[i][lines[i].index(': ')+2:].strip()
		d[k] = v
		# if k == 'URL':
		# 	url = v
		# elif k == 'TITLE':
		# 	booktitle = v
		# elif k == "ADDRESS":
		# 	addr = v
		# elif k == "YEAR":
		# 	year = v
		# elif k == "KEY":
		# 	keystart = v
		# elif k == "VENUE":
		# 	venue = v
		# else:
		# 	print('Unknown @key:', k, 'valued', v)
		i += 1
	title = lines[i].strip().replace('  ', ' ')
	auths = lines[i+1].strip().split(', ')
	if lines[i+2].strip() != '':
		url = lines[i+2].strip()
		i += 1
	else:
		url = ''
	assert lines[i+2].strip() == ''
	cx += 1
	key = keystart + '-' + deentitify(auths[0].split(' ')[-1])
	if len(auths) > 1:
		for a in auths[1:]:
			key += a.split(' ')[-1][0]
	if key in used:
		dx = 1
		while '{}{}'.format(key, dx) in used:
			dx += 1
		key = '{}{}'.format(key, dx)
		# key += 'a'
		# while key in used:
		# 	key = key[:-1] + chr(ord(key[-1])+1)
	print(key)
	used.append(key)
	f = open(keystart + '/'+key+'.json', 'w')
	opts = ''
	for opt in d.keys():
		if opt not in ('TITLE', 'URL'):
			opts += '\n\t"{l}": {v},'.format(l=opt.lower(), v=d[opt])
	if url:
		'\n\t"{l}": {v},'.format(l="url", v=url)
	f.write('''{{{optionals}
	"booktitle": {bt},
	"type": "inproceedings",
	"title": "{title}",
	"author": {authors},
	"pages": {pages}
}}
'''.format(\
	optionals=opts,
	title=title,
	bt=d['TITLE'],
	authors=js(auths),
	pages=cx))
	f.close()
	i += 3
print(cx, 'papers processed')
f = open(keystart +'.json', 'w')
opts = ''.join(['\n\t"{l}": {v},'.format(l=opt.lower(), v=d[opt]) for opt in d.keys()])
f.write('{{{optionals}\n\t"type": "proceedings"\n}}\n'.format(optionals=opts))
f.close()
