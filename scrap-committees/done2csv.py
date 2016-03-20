#!/c/Users/vadim/AppData/Local/Programs/Python/Python35/python
# -*- coding: utf-8 -*-
#
# a module to create a CSV

import sys
sys.path.append('..')
from fancy.ANSI import C

ROLEZ = {\
	'AwCh': 'Award Chair',
	'BrCh': 'Briefings Chair',
	'DaCh': 'Data Chair',
	'DSCh': 'Doctoral Symposium Chair',
	'PSCh': 'Post-Doctoral Symposium Chair',
	'ERCh': 'ERA Track Chair',
	'ERCo': 'ERA Track Program Committee',
	'ERP' : 'Expert Review Panel',
	'FiCh': 'Finance Chair',
	'ChCh': 'Challenge Chair',
	'ChCo': 'Challenge Committee',
	'GeCh': 'General Chair',
	'InCh': 'Industrial Track Chair',
	'ITPC': 'Industrial Track Program Committee',
	'KN':   'Keynote Speaker',
	'LoCh': 'Local Chair',
	'LoCo': 'Local Committee',
	'MoCh': 'Mobile Chair',
	'OrCh': 'Organising Chair',
	# 'OrCo': 'Organiser',
	'OrCo': 'Organising Committee',
	'PaCh': 'Panel Chair',
	'PbCh': 'Publicity Chair',
	'PBCh': 'Program Board Chair',
	'PBCo': 'Program Board',
	'PjCh': 'Project Chair',
	'PoCh': 'Poster Chair',
	'PrCh': 'Program Chair',
	'PrCo': 'Program Committee',
	'PuCh': 'Publication Chair',
	'SaCh': 'Satellite Events Chair',
	'ScCo': 'Scientific Committee',
	'ScLi': 'Scientific Liaison',
	'SMCh': 'Social Media Chair',
	'SRCh': 'Student Research Competition Chair',
	'SpCh': 'Sponsor Chair',
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

CONFZ = {\
	'FOSE': 'FoSE',
	'MODELS': 'MoDELS'\
}

BLANK = '     '
lines = []
cur = ''
for fn in sys.argv[1:-1]:
	if cur != fn.split('-')[0]:
		if cur != '':
			print()
		name = fn.split('-')[0].upper()
		if name in CONFZ:
			name = CONFZ[name]
		print('[{}]'.format(C.green(name)), end=': ')
		cur = fn.split('-')[0]
	print("'{}".format(fn.split('-')[-1][-6:-4]), end=' ')
	f = open(fn, 'r', encoding='utf-8')
	lines += [(fn, line[:5], line[5:].strip()) for line in f.readlines()\
		if line.strip() and line[:5] != BLANK and not line.startswith('#DONE')]
	f.close()
print()

succ = fail = 0
males = set(line.strip() for line in open('../naming/male.txt', 'r', encoding='utf-8').readlines())
femes = set(line.strip() for line in open('../naming/female.txt', 'r', encoding='utf-8').readlines())
asexs = set()

f = open(sys.argv[-1], 'w', encoding='utf-8')

for line in lines:
	fn, status, name = line
	for sep in ('\t', ',', '('):
		if sep in name:
			name = name.split(sep)[0]
	if name.startswith('* ') or name.startswith('- '):
		name = name[2:].strip()
	if name.startswith('Prof.'):
		name = name[5:].strip()
	if name.startswith('Dr.'):
		name = name[3:].strip()
	if name.count(' ') > 2:
		name = name.split('   ')[0]
	# Conference;Year;First Name;Last Name;Sex;Role
	conf = fn.split('-')[0].upper().replace('_', '-')
	if conf in CONFZ.keys():
		conf = CONFZ[conf]
	year = fn.split('-')[1].split('.')[0]
	fname = name.split(' ')[0].strip()
	lname = ' '.join(name.split(' ')[1:]).strip()
	if lname.find(' - '):
		lname = lname.split(' - ')[0]
	role = ROLEZ[status.strip()]
	# try to determine gender
	if fname in males:
		gender = 'Male'
		succ += 1
	elif fname in femes:
		gender = 'Female'
		succ += 1
	else:
		gender = ''
		asexs.add(fname)
		fail += 1
	# line = fn, status, name
	# print(line)
	f.write('{};{};{};{};{};{}\n'.format(conf, year, fname, lname, gender, role))
f.close()

open('../naming/unknown.txt', 'w', encoding='utf-8').write('\n'.join(sorted(asexs)))

# safeguard
if fail == 0 and succ == 0:
	fail = 1
print('With {} known names, {}% was classified.'.format(len(males)+len(femes), 100*succ//(succ+fail)))
