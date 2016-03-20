#!/c/Users/vadim/AppData/Local/Programs/Python/Python35/python
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

def match1(s, sub):
	return s.lower().find(sub.lower()) > -1

def match(s, sub):
	return match1(s,sub) and not match1(s, '('+sub+')') and not match1(s, ' - '+sub)

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
f = open(sys.argv[1], 'r', encoding='utf-8')
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
	'France',
	'SLE Workshops are handled through SPLASH',
	'Name	email	Web site	organization	role',
	'name	email	Web site	organization	role'\
)

ignopatterns = (\
	'Organizing', 'Committee', 'College', 'Technology', 'École', 'Ecole',
	'Universidade', 'Université', 'Universidad', 'University',
	'Vrije Universiteit', 'Polytechnique', 'Microsoft', 'Semantic Designs',
	'Dresden', 'Macquarie', 'Eindhoven', 'Clemson', 'Lancaster',
	'INRIA', '-----', '=====', 'Organization', 'Netherlands',
	'IBM', 'CWI', 'PathBridge', 'Simula',
	'Centrum voor Wiskunde en Informatica', 'Centrum Wiskunde & Informatica',
	'The Netherlands', 'Faculty', 'TU Delft',
	'Interactive Software Development', 'Kruislaan', 'NL-1098', 'Smetanova',
	'Slovenia', 'http://' \
)
BLANK = '     '
mode = BLANK
for i in range(0, len(lines)):
	status, line = lines[i]
	if len(line) > 200 or len(line) < 2:
		status = BLANK
	elif matchbeg(line, ('(', '???', '//')):
		status = BLANK
	elif match(line, 'Name') and match(line, 'Surname'):
		status = BLANK
	elif matchs(line, ('PC co-chairs', 'Program Chair', 'Program co-chairs',\
	'Program Committee Co-chairs', 'Research Track Co-chairs', 'Program Chairs',\
	'PC CHAIRS', 'PC chairs', 'Programme Chairs')):
		status, mode = BLANK, 'PrCh '
	elif matchs(line, ('Publicity chair', 'Publicity Co-Chairs')) \
		and not match(line, 'Publicity chair, '):
		status, mode = BLANK, 'PbCh '
	elif matchs(line, ('Local organization chair', 'Local arrangements and registration',\
		'Local Co-chairs', 'Local Arrangement Chair', 'Local Organizing Chair',\
		'Local Facilities Chairs', 'Local Chair', 'Local Organisation Chair',\
		'Social Event Co-Chairs', 'Registration Co-Chairs')):
		status, mode = BLANK, 'LoCh '
	elif matchs(line, ('Local Organizing Team', 'Local Arrangements')):
		status, mode = BLANK, 'LoCo '
	elif matchs(line, ('Panel organization chair', 'Panel Co-chairs',\
		'Panel Chair')):
		status, mode = BLANK, 'PaCh '
	elif matchs(line, ('Post-Doctoral Symposium Co-Chairs',)):
		status, mode = BLANK, 'PSCh '
	elif matchs(line, ('DOCTORAL SYMPOSIUM CHAIR',\
		'Doctoral Symposium Co-Chairs', 'Doctoral Symposium Track Co-chairs')):
		status, mode = BLANK, 'DSCh '
	elif matchs(line, ('Student volunteers coordinator',\
		'Student-volunteer Chair', 'Student Volunteers Chairs',\
		'Student Volunteers Chair', 'Student Volunteers Co-Chairs')):
		status, mode = BLANK, 'SVCh '
	elif matchs(line, ('MIP Award Chair',)):
		status, mode = BLANK, 'AwCh '
	elif match(line, 'Student Research Competition Chair'):
		status, mode = BLANK, 'SRCh '
	elif matchs(line, ('Finance Co-chairs', 'Liaison Chairs - Finances',\
		'Financial Chairs', 'Finance Chair', 'Finances Chair')):
		status, mode = BLANK, 'FiCh '
	elif matchs(line, ('ERA Track Co-chairs', 'ERA Chairs', 'ERA Co-Chairs',\
		'ERA Track Chairs')):
		status, mode = BLANK, 'ERCh '
	elif matchs(line, ('ERA Track Committee',)):
		status, mode = BLANK, 'ERCo '
	elif match(line, 'Challenge Chair'):
		status, mode = BLANK, 'ChCh '
	elif match(line, 'Hackathon Chair'):
		status, mode = BLANK, 'HaCh '
	elif matchs(line, ('Tutorials Co-chairs', 'Tutorial Co-Chairs',\
		'Tutorial Chairs', 'Tutorials Chair')):
		status, mode = BLANK, 'TuCh '
	elif matchs(line, ('Data Chair', 'Chief of Data')):
		status, mode = BLANK, 'DaCh '
	elif match(line, 'Satellite Events'):
		status, mode = BLANK, 'SaCh '
	elif match(line, 'Vision Papers'):
		status, mode = BLANK, 'ViCh '
	elif match(line, 'Project Track'):
		status, mode = BLANK, 'PjCh '
	elif matchs(line, ('Poster Chairs', 'Poster Chair', 'Poster Co-Chairs')):
		status, mode = BLANK, 'PoCh '
	elif matchs(line, ('Proceedings Chair', 'Proceedings Co-chairs',\
		'Liaison Chairs - Publications', 'Publication Chair',\
		'Publications Chair')):
		status, mode = BLANK, 'PuCh ' # == Publication Chair
	elif matchs(line, ('Invited Speaker', 'Keynote Speaker', 'Keynotes',\
		'Keynote Talks')):
		status, mode = BLANK, 'KN   '
	elif match(line, 'Important Dates'):
		status, mode = BLANK, BLANK
	elif matchs(line, ('Mobile Chair', 'Mobile Web Chair')):
		status, mode = BLANK, 'MoCh '
	elif match(line, 'Expert Review Panel'):
		status, mode = BLANK, 'ERP  '
	elif matchs(line, ('Tool Demonstrations Program Committee',\
		'Tool track program committee')):
		status, mode = BLANK, 'TTPC '
	elif matchs(line, ('Tool Demonstrations Chairs', 'Demonstrations Chair',\
		'Demonstrations Chairs', 'Demonstration Chairs',\
		'Tool Demonstration Co-Chairs', 'Tool Demo Co-Chairs',\
		'Tool Demonstrations Track Chairs', 'Tools Track Co-chair')):
		status, mode = BLANK, 'TTCh '
	elif match(line, 'Industry track program committee'):
		status, mode = BLANK, 'ITPC '
	elif matchs(line, ('Industry Track', 'Industrial Track Co-chair',\
		'Industry Liaison', 'Industrial Liaison Chair')):
		status, mode = BLANK, 'InCh '
	elif match(line, 'Scientific Liason'):
		status, mode = BLANK, 'ScLi '
	elif matchs(line, ('Program committee', 'PROGRAM COMITTEE', 'Programme Committee')):
		status, mode = BLANK, 'PrCo '
	elif match(line, 'Program Board'):
		status, mode = BLANK, 'PBCo '
	elif match(line, 'Scientific committee'):
		status, mode = BLANK, 'ScCo '
	elif match(line, 'Steering Committee Chair'):
		status, mode = BLANK, 'StCh '
	elif match(line, 'Steering committee'):
		status, mode = BLANK, 'StCo '
	elif match(line, 'Challenge Committee'):
		status, mode = BLANK, 'ChCo '
	elif match(line, 'Sponsor Chairs'):
		status, mode = BLANK, 'SpCh '
	elif matchs(line, ('Publicity-chair - Social media-chair',\
		'Social Chair', 'Social Media Chairs', 'Social Media Chair')):
		status, mode = BLANK, 'SMCh '
	elif matchs(line, ('Workshop organization chair', 'Workshop co-Chairs',\
		'Workshops Co-chair', 'Workshops', 'Workshop Chairs')):
		status, mode = BLANK, 'WoCh '
	elif matchs(line, ('General chair', 'Conference chair')):
		status, mode = BLANK, 'GeCh '
		# TODO: do we really care to distinguish GeCh from OrCh?
	elif match(line, 'Organization Chair'):
		status, mode = BLANK, 'OrCh '
	elif matchs(line, ('ORGANIZATION COMMITTEE', 'organizing committee',\
		'Organizers', 'Organisation Committee', 'Organizing & Steering')):
		status, mode = BLANK, 'OrCo '
	elif matchs(line, ('Website administration', 'Web Chair', 'Webmaster', 'Web Co-Chairs')):
		status, mode = BLANK, 'WeCh '
	elif matchbeg(line, ignopatterns):
		status = BLANK
	elif matchs(line, ignopatterns)\
	and ',' not in line and '\t' not in line and '(' not in line:
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
		if matchs(line, ('(chair)', '(co-chair)', ', chair', ', co-chair', '(Vice Chair)')):
			# line = line.replace('(chair)', '').strip()
			status = status.replace('Co', 'Ch')
		elif matchs(line, ('(General Chair)', '- General Chair')):
			status = 'GeCh '
		elif match(line, '(Finance Chair)'):
			status = 'FiCh '
		elif match(line, '(Challenge Chair)'):
			status = 'ChCh '
		elif matchs(line, ('Publicity Chair, ', ' - Publicity Chair', \
			'(Publicity co-Chair)', '(Publicity Chair)')):
			status = 'PbCh '
		elif match(line, '(Workshop Selection Chair)'):
			status = 'WoCh '
		elif matchs(line, ('(Program Chair)', '(Program co-Chair)', '- Program Chair')):
			status = 'PrCh '
		elif matchs(line, ('(Organizing Chair)', '- Organization Chair')):
			status = 'OrCh '
		elif match(line, '(Tutorials Chair)'):
			status = 'TuCh '
		elif match(line, '- Briefings Chair'):
			status = 'BrCh '
		elif match(line, '- Industry Chair'):
			status = 'InCh '
		elif matchs(line, ('(Web Chair)', '(Web and Publicity co-Chair)', '(web)')):
			status = 'WeCh '
		elif match(line, '(social media)'):
			status = 'SMCh '
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

f = open(sys.argv[1], 'w', encoding='utf-8')
f.write('#DONE\n')
for status, line in lines:
	f.write(status+line+'\n')
f.close()
