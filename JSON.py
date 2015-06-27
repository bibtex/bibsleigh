#!/usr/local/bin/python3

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
	else:
		print('Unknown JSON type in', s)
		return '"{}"'.format(s)

def jsonkv(k, v):
	return jsonify(k) + ': ' + jsonify(v)
