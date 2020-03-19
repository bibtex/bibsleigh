#!/c/Users/vadim/AppData/Local/Programs/Python/Python37-32/python
# -*- coding: utf-8 -*-

import json
from fancy.ANSI import C
from lib.NLP import strictstrip
from collections import Counter

def jsonify(s):
	if isinstance(s, int):
		return '{}'.format(s)
	elif isinstance(s, str):
		return '"{}"'.format(s)
	elif isinstance(s, list):
		if s and isinstance(s[0], list):
			return '[' + ',\n\t\t'.join([jsonify(x) for x in s]) + ']'
		return '[' + ', '.join([jsonify(x) for x in s]) + ']'
	elif isinstance(s, tuple):
		return '[' + ', '.join([jsonify(x) for x in s]) + ']'
	elif isinstance(s, Counter):
		# a trick to remove zero-time elements
		s += Counter()
		pairs = [jsonify(k) + ', ' + jsonify(s[k]) for k in sorted(s.keys())]
		return '[' + ', '.join(pairs) + ']'
	elif isinstance(s, set):
		return '[' + ', '.join([jsonify(x) for x in sorted(s)]) + ']'
	elif isinstance(s, dict):
		return '{\n' + ',\n'.join(['\t"{k}": {v}'.format(k=k, v=jsonify(s[k])) \
			for k in sorted(s.keys())]) + '\n}\n'
	else:
		print('Unknown JSON type in', s)
		return '"{}"'.format(s)

def jsonkv(k, v):
	return jsonify(k) + ': ' + jsonify(v)

def parseJSON(fn):
	# print('Parsing',fn,'...')
	try:
		j = json.load(open(fn, 'r', encoding='utf-8'))
		j['FILE'] = fn
		return j
	except ValueError:
		print(C.red('JSON parse error'), 'on', fn.replace('\\', '/'))
		return {}

def json2lines(j):
	res = []
	for line in j:
		line = strictstrip(line)
		if line in ('', '{', '}'):
			continue
		if line.startswith('"'):
			res.append(line)
		else:
			res[-1] += line
	return res
