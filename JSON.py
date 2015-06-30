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

def parseJSON(fn):
	dct = {}
	f1 = open(fn, 'r')
	for line in f1.readlines():
		line = line.strip()
		if line in ('{', '}', '') or line.startswith('//'):
			continue
		if line.endswith(','):
			line = line[:-1]
		perq = line.split('"')
		if len(perq) == 5:
			dct[perq[1]] = perq[3]
		elif len(perq) == 3:
			dct[perq[1]] = int(perq[-1][2:])
		elif len(perq) != 5 and perq[1] in ('title', 'booktitle'):
			# tolerance to quotes in titles
			rawtail = line.replace('"'+perq[1]+'": ', '')
			dct[perq[1]] = rawtail[rawtail.index('"')+1 : rawtail.rindex('"')]
		elif len(perq) > 5:
			dct[perq[1]] = [z for z in perq[3:-1] if z != ', ']
		else:
			print('Skipped line', line, 'in', fn)
	f1.close()
	dct['FILE'] = fn
	return dct
