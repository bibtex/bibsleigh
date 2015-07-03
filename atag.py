#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for creating a simplistic tag definition

import sys

tag = ' '.join(sys.argv[1:])
f = open('../json/tags/'+tag+'.json', 'w')
if tag.find(' ') < 0:
	m = 'matchword'
else:
	m = 'matchsub'
f.write('{{\n\t"name": "{0}",\n\t"{1}": ["{0}"]\n}}\n'.format(tag, m))
f.close()
