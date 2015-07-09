#!/usr/local/bin/python3

import json

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
	j = json.load(open(fn, 'r'))
	j['FILE'] = fn
	return j
