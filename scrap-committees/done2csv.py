#!/c/Users/vadim/AppData/Local/Programs/Python/Python35/python
# -*- coding: utf-8 -*-
#
# a module to create a CSV

import sys
sys.path.append('..')
from fancy.ANSI import C

ROLEZ = {\
	'AdviceCo'  :  'Advisory Committee',
	'AwardCh'   :  'Award Chair',
	'BriefCh'   :  'Briefings Chair',
	'ChalngCh'  :  'Challenge Chair',
	'ChalngCo'  :  'Challenge Committee',
	'DataCh'    :  'Data Chair',
	'DemoCh'    :  'Demo Track Chair',
	'DemoCo'    :  'Demo Track Program Committee',
	'DocSymCh'  :  'Doctoral Symposium Chair',
	'DocSymCo'  :  'Doctoral Symposium Program Committee',
	'EarlyCh'   :  'Early Research Track Chair',
	'EarlyCo'   :  'Early Research Track Program Committee',
	'FinanceCh' :  'Finance Chair',
	'GeneralCh' :  'General Chair',
	'HackCh'    :  'Hackathon Chair',
	'KeyNote'   :  'Keynote Speaker',
	'LocRegCh'  :  'Local Chair',
	'LocRegCo'  :  'Local Committee',
	'MobileCh'  :  'Mobile Chair',
	'OrganCh'   :  'Organising Chair',
	'OrganCo'   :  'Organising Committee',
	'PanelCh'   :  'Panel Chair',
	'PodSymCh'  :  'Post-Doctoral Symposium Chair',
	'PosterCh'  :  'Poster Chair',
	'PractCh'   :  'Practical Track Chair',
	'PractCo'   :  'Practical Track Program Committee',
	'ProgBoCh'  :  'Program Board Chair',
	'ProgBoCo'  :  'Program Board',
	'ProgramCh' :  'Program Chair',
	'ProgramCo' :  'Program Committee',
	'ProjectCh' :  'Project Chair',
	'PublicaCh' :  'Publication Chair',
	'PubRelCh'  :  'Publicity Chair',
	'SatellCh'  :  'Satellite Events Chair',
	'ScienceCo' :  'Scientific Committee',
	'ScientLi'  :  'Scientific Liaison',
	'SocMedCh'  :  'Social Media Chair',
	'SponsorCh' :  'Sponsor Chair',
	'SteerCh'   :  'Steering Chair',
	'SteerCo'   :  'Steering Committee',
	'StudComCh' :  'Student Research Competition Chair',
	'StudentCh' :  'Student Volunteers Chair',
	'TutorCh'   :  'Tutorials Chair',
	'VisionCh'  :  'Vision Chair',
	'WebCh'     :  'Web Chair',
	'WorkspCh'  :  'Workshop Chair',\
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
	lines += [(fn, line[:10], line[10:].strip()) for line in f.readlines()\
		if line.strip() \
		and line[:10] != '          ' \
		and not line.startswith('##########')]
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
	for sep in '-–—':
		if lname.find(' '+sep+' '):
			lname = lname.split(' '+sep+' ')[0]
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
