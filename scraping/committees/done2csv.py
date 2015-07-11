#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module to create a CSV

import sys

ROLEZ = {\
	'DSCh': 'Doctoral Symposium Chair',
	'FiCh': 'Finance Chair',
	'GeCh': 'General Chair',
	'KN':   'Keynote Speaker',
	'LoCh': 'Local Chair',
	'OrCo': 'Organiser',
	'PaCh': 'Panel Chair',
	'PbCh': 'Publicity Chair',
	'PrCh': 'Program Chair',
	'PrCo': 'Program Committee',
	'PuCh': 'Publication Chair',
	'StCh': 'Steering Chair',
	'StCo': 'Steering Committee',
	'WeCh': 'Web Chair',
	'WoCh': 'Workshop Chair',\
}

BLANK = '     '
lines = []
for fn in sys.argv[1:]:
	f = open(fn, 'r')
	lines += [(fn, line[:5], line[5:].strip()) for line in f.readlines()\
		if line[:5] != BLANK and not line.startswith('#DONE')]
	f.close()

for line in lines:
	fn, status, name = line
	if ',' in name:
		name = name.split(',')[0]
	if '(' in name:
		name = name.split('(')[0]
	# Conference;Year;First Name;Last Name;Sex;Role
	conf = fn.split('-')[0].upper()
	year = fn.split('-')[1].split('.')[0]
	fname = name.split(' ')[0]
	lname = ' '.join(name.split(' ')[1:])
	role = ROLEZ[status.strip()]
	# line = fn, status, name
	# print(line)
	print('{};{};{};{};;{}'.format(conf, year, fname, lname, role))
