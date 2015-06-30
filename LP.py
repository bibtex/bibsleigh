#!/usr/local/bin/python3
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
