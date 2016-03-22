#!/c/Users/vadim/AppData/Local/Programs/Python/Python35/python
# -*- coding: utf-8 -*-
#
# a module for list processing

def uniq(xs):
	rs = []
	for x in xs:
		if x not in rs:
			rs.append(x)
	return rs

def listify(y):
	return y if isinstance(y, list) else [y]

# these ones are needed for windows-unix compatibility
def lastSlash(s):
	return s.split('/')[-1].split('\\')[-1]

def getPath(s):
	res = []
	for x in s.split('/'):
		for y in x.split('\\'):
			res.append(y)
	return res
