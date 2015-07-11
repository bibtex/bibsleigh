#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module to make sense out of CfPs or webpage scraps

import sys

def colour(c, s):
	return '{}{}{}'.format(c, s, '\033[0m')

def ye(s):
	return colour('\033[93m', s)
def pu(s):
	return colour('\033[95m', s)

# 	ENDC = '\033[0m'
# 	BOLD = '\033[1m'
# 	ULINE = '\033[4m'
# 	RED = '\033[91m'
# 	GREEN = '\033[92m'
# 	YELLOW = '\033[93m'
# 	BLUE = '\033[94m'
# 	PURPLE = '\033[95m'

def match(s, sub):
	return s.lower().find(sub.lower()) > -1

def matchs(s, subs):
	for sub in subs:
		if match(s, sub):
			return True
	return False

def matchbeg(s, subs):
	for sub in subs:
		if s.lower().startswith(sub.lower()):
			return True
	return False

lines = []
done = False
f = open(sys.argv[1], 'r')
for line in f.readlines():
	if line.startswith('#DONE'):
		done = True
		continue
	if done:
		lines.append([line[:5], line[5:].strip()])
	else:
		lines.append(['     ', line.strip()])
f.close()


ignored = (\
	'SLE Workshops are handled through SPLASH'\
)

ignopatterns = (\
	'Universidade', 'CWI', 'University', 'Dresden', 'Macquarie', 'Eindhoven', 'Clemson', 'Lancaster',
	'INRIA', '-----', 'Organization'\
)
BLANK = '     '
mode = BLANK
for i in range(0, len(lines)):
	status, line = lines[i]
	if match(line, 'General chair'):
		status, mode = BLANK, 'GeCh '
	elif matchs(line, ('PC co-chairs', 'Program co-chairs', 'Program Committee Co-chairs')):
		status, mode = BLANK, 'PrCh '
	elif match(line, 'Publicity chair') and not match(line, 'Publicity chair, '):
		status, mode = BLANK, 'PbCh '
	elif match(line, 'Local organization chair'):
		status, mode = BLANK, 'LoCh '
	elif match(line, 'Panel organization chair'):
		status, mode = BLANK, 'PaCh '
	elif match(line, 'DOCTORAL SYMPOSIUM CHAIR'):
		status, mode = BLANK, 'DSCh '
	elif matchs(line, ('Invited Speakers', 'Keynote Speakers')):
		status, mode = BLANK, 'KN   '
	elif match(line, 'Important Dates'):
		status, mode = BLANK, BLANK
	elif matchs(line, ('Program committee', 'PROGRAM COMITTEE')):
		status, mode = BLANK, 'PrCo '
	elif match(line, 'Steering committee'):
		status, mode = BLANK, 'StCo '
	elif matchs(line, ('ORGANIZATION COMMITTEE', 'organizing committee')):
		status, mode = BLANK, 'OrCo '
	elif match(line, 'Workshop organization chair'):
		status, mode = BLANK, 'WoCh '
	elif matchbeg(line, ignopatterns):
		status = BLANK
	elif line in ignored:
		status = BLANK
	elif ' ' not in line and '@' in line:
		status = BLANK
	else:
		# 
		if mode != BLANK:
			status = mode
		if matchs(line, ('(chair)', '(co-chair)')):
			# line = line.replace('(chair)', '').strip()
			status = status.replace('Co', 'Ch')
		elif match(line, '(Finance Chair)'):
			status = 'FiCh '
		elif matchs(line, ('Publicity co-Chair)', 'Publicity Chair, ')):
			status = 'PuCh '
		elif match(line, '(Workshop Selection Chair)'):
			status = 'WoCh '
		elif match(line, '(Web Chair)'):
			status = 'WeCh '
	lines[i] = [status, line]

# # ws = line.strip().split()
# # nws = []
# # for w in ws:
# # 	if match(w, 'committee') or match(w, 'chair'):
# # 		nws.append(pu(w))
# # 	else:
# # 		nws.append(w)
# # line = ' '.join(nws)
# print(line)

f = open(sys.argv[1], 'w')
f.write('#DONE\n')
for status, line in lines:
	f.write(status+line+'\n')
f.close()
