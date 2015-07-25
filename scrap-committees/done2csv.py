#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module to create a CSV

import sys

ROLEZ = {\
	'BrCh': 'Briefings Chair',
	'DSCh': 'Doctoral Symposium Chair',
	'ERCh': 'ERA Track Chair',
	'FiCh': 'Finance Chair',
	'GeCh': 'General Chair',
	'InCh': 'Industrial Track Chair',
	'ITPC': 'Industrial Track Program Committee',
	'KN':   'Keynote Speaker',
	'LoCh': 'Local Chair',
	'OrCh': 'Organising Chair',
	# 'OrCo': 'Organiser',
	'OrCo': 'Organising Committee',
	'PaCh': 'Panel Chair',
	'PbCh': 'Publicity Chair',
	'PjCh': 'Project Chair',
	'PrCh': 'Program Chair',
	'PrCo': 'Program Committee',
	'PuCh': 'Publication Chair',
	'SaCh': 'Satellite Events Chair',
	'ScCo': 'Scientific Committee',
	'SMCh': 'Social Media Chair',
	'StCh': 'Steering Chair',
	'StCo': 'Steering Committee',
	'SVCh': 'Student Volunteers Chair',
	'TTCh': 'Tool Track Chair',
	'TTPC': 'Tool Track Program Committee',
	'TuCh': 'Tutorials Chair',
	'ViCh': 'Vision Chair',
	'WeCh': 'Web Chair',
	'WoCh': 'Workshop Chair',\
}

BLANK = '     '
lines = []
for fn in sys.argv[1:]:
	f = open(fn, 'r')
	lines += [(fn, line[:5], line[5:].strip()) for line in f.readlines()\
		if line.strip() and line[:5] != BLANK and not line.startswith('#DONE')]
	f.close()

for line in lines:
	fn, status, name = line
	for sep in ('\t', ',', '('):
		if sep in name:
			name = name.split(sep)[0]
	if name.startswith('* ') or name.startswith('- '):
		name = name[2:].strip()
	if name.count(' ') > 2:
		name = name.split('   ')[0]
	# Conference;Year;First Name;Last Name;Sex;Role
	conf = fn.split('-')[0].upper().replace('_', '-')
	year = fn.split('-')[1].split('.')[0]
	fname = name.split(' ')[0].strip()
	lname = ' '.join(name.split(' ')[1:]).strip()
	role = ROLEZ[status.strip()]
	# line = fn, status, name
	# print(line)
	print('{};{};{};{};;{}'.format(conf, year, fname, lname, role))
