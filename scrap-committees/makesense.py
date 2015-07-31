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
	'SLE Workshops are handled through SPLASH',
	'Name	email	Web site	organization	role',
	'name	email	Web site	organization	role'\
)

ignopatterns = (\
	'Organizing', 'Committee',
	'Universidade', 'CWI', 'University', 'Dresden', 'Macquarie', 'Eindhoven', 'Clemson', 'Lancaster',
	'INRIA', '-----', '=====', 'Organization', 'Netherlands', 'Centrum voor Wiskunde en Informatica',
	'France', 'Interactive Software Development', 'Kruislaan', 'NL-1098', 'The Netherlands', 'Faculty', 
	'Smetanova', 'Slovenia', 'http://' \
)
BLANK = '     '
mode = BLANK
for i in range(0, len(lines)):
	status, line = lines[i]
	if len(line) > 200 or len(line) < 2:
		status = BLANK
	elif line.startswith('???'):
		status = BLANK
	elif line.startswith('('):
		status = BLANK
	elif match(line, 'Name') and match(line, 'Surname'):
		status = BLANK
	elif matchs(line, ('General chair', 'Conference chair', 'Organization Chair')):
		status, mode = BLANK, 'GeCh '
	elif matchs(line, ('PC co-chairs', 'Program Chair', 'Program co-chairs',\
	'Program Committee Co-chairs', 'Research Track Co-chairs', 'Program Chairs',\
	'PC CHAIRS', 'PC chairs', 'Programme Chairs')):
		status, mode = BLANK, 'PrCh '
	elif match(line, 'Publicity chair') and not match(line, 'Publicity chair, '):
		status, mode = BLANK, 'PbCh '
	elif matchs(line, ('Local organization chair', 'Local arrangements and registration',\
		'Local Co-chairs', 'Local Arrangement Chair')):
		status, mode = BLANK, 'LoCh '
	elif matchs(line, ('Panel organization chair', 'Panel Co-chairs')):
		status, mode = BLANK, 'PaCh '
	elif matchs(line, ('DOCTORAL SYMPOSIUM CHAIR', 'Doctoral Symposium Track Co-chairs')):
		status, mode = BLANK, 'DSCh '
	elif matchs(line, ('Student-volunteer Chair', 'Student volunteers coordinator')):
		status, mode = BLANK, 'SVCh '
	elif matchs(line, ('Finance Co-chairs', 'Liaison Chairs - Finances')):
		status, mode = BLANK, 'FiCh '
	elif matchs(line, ('ERA Track Co-chairs', 'ERA Chairs')):
		status, mode = BLANK, 'ERCh '
	elif match(line, 'Challenge Chair'):
		status, mode = BLANK, 'ChCh '
	elif match(line, 'Hackathon Chair'):
		status, mode = BLANK, 'HaCh '
	elif match(line, 'Tutorials Co-chairs'):
		status, mode = BLANK, 'TuCh '
	elif matchs(line, ('Data Chair', 'Chief of Data')):
		status, mode = BLANK, 'DaCh '
	elif match(line, 'Satellite Events'):
		status, mode = BLANK, 'SaCh '
	elif match(line, 'Vision Papers'):
		status, mode = BLANK, 'ViCh '
	elif match(line, 'Project Track'):
		status, mode = BLANK, 'PjCh '
	elif matchs(line, ('Proceedings Chair', 'Proceedings Co-chairs', 'Liaison Chairs - Publications', 'Publication Chair')):
		status, mode = BLANK, 'PuCh ' # == Publication Chair
	elif matchs(line, ('Invited Speaker', 'Keynote Speaker')):
		status, mode = BLANK, 'KN   '
	elif match(line, 'Important Dates'):
		status, mode = BLANK, BLANK
	elif match(line, 'Tool track program committee'):
		status, mode = BLANK, 'TTPC '
	elif match(line, 'Tool Demonstrations Chairs'):
		status, mode = BLANK, 'TTCh '
	elif match(line, 'Industry track program committee'):
		status, mode = BLANK, 'ITPC '
	elif matchs(line, ('Industry Track', 'Industrial Track Co-chair')):
		status, mode = BLANK, 'InCh '
	elif matchs(line, ('Program committee', 'PROGRAM COMITTEE', 'Programme Committee')):
		status, mode = BLANK, 'PrCo '
	elif match(line, 'Scientific committee'):
		status, mode = BLANK, 'ScCo '
	elif match(line, 'Steering committee'):
		status, mode = BLANK, 'StCo '
	elif match(line, 'Challenge Committee'):
		status, mode = BLANK, 'ChCo '
	elif matchs(line, ('Publicity-chair - Social media-chair', 'Social Chair')):
		status, mode = BLANK, 'SMCh '
	elif matchs(line, ('ORGANIZATION COMMITTEE', 'organizing committee', 'Organizers', 'Organisation Committee', 'Organizing & Steering')):
		status, mode = BLANK, 'OrCo '
	elif matchs(line, ('Workshop organization chair', 'Workshop co-Chairs', 'Workshops Co-chair', 'Workshops')):
		status, mode = BLANK, 'WoCh '
	elif matchs(line, ('Website administration', 'Web Chair', 'Webmaster')):
		status, mode = BLANK, 'WeCh '
	elif matchbeg(line, ignopatterns):
		status = BLANK
	elif line.split(' ')[0].isdigit():
		status = BLANK
	elif line in ignored:
		status = BLANK
	elif (' ' not in line and '@' in line) or \
		(line.find(' at ') > -1 and ' ' not in line.replace(' at ', '')):
		status = BLANK
	else:
		# 
		if mode != BLANK:
			status = mode
		if matchs(line, ('(chair)', '(co-chair)', ', chair', ', co-chair')):
			# line = line.replace('(chair)', '').strip()
			status = status.replace('Co', 'Ch')
		elif match(line, '(Finance Chair)'):
			status = 'FiCh '
		elif match(line, '(Challenge Chair)'):
			status = 'ChCh '
		elif matchs(line, ('Publicity Chair, ', ' - Publicity Chair')):
			status = 'PbCh '
		elif match(line, '(Workshop Selection Chair)'):
			status = 'WoCh '
		elif matchs(line, ('(Program Chair)', '(Program co-Chair)')):
			status = 'PrCh '
		elif match(line, '(Organizing Chair)'):
			status = 'OrCh '
		elif match(line, '(Tutorials Chair)'):
			status = 'TuCh '
		elif matchs(line, ('(Web Chair)', '(Web and Publicity co-Chair')):
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
