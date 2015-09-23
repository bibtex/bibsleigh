#!/usr/local/bin/python3

import json
from fancy.ANSI import C
from lib.NLP import strictstrip

def jsonify(s):
	if isinstance(s, int):
		return '{}'.format(s)
	elif isinstance(s, str):
		if s.isdigit():
			# return '{}'.format(s)
			return '"{}"'.format(s)
		else:
			return '"{}"'.format(s)
	elif isinstance(s, list):
		if s and isinstance(s[0], list):
			return '[' + ',\n\t\t'.join([jsonify(x) for x in s]) + ']'
		return '[' + ', '.join([jsonify(x) for x in s]) + ']'
	elif isinstance(s, dict):
		return '{\n' + ',\n'.join(['\t"{k}": {v}'.format(k=k, v=jsonify(s[k])) for k in sorted(s.keys())]) + '\n}\n'
	else:
		print('Unknown JSON type in', s)
		return '"{}"'.format(s)

def jsonkv(k, v):
	return jsonify(k) + ': ' + jsonify(v)

def parseJSON(fn):
	# print('Parsing',fn,'...')
	try:
		j = json.load(open(fn, 'r'))
		j['FILE'] = fn
		return j
	except ValueError:
		print(C.red('JSON parse error'), 'on', fn)
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
