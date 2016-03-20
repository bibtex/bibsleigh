#!/c/Users/vadim/AppData/Local/Programs/Python/Python35/python
# -*- coding: utf-8 -*-
#
# a module to make sense out of CfPs or webpage scraps

import sys

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
	if line.startswith('##########'):
		done = True
		continue
	if done:
		lines.append([line[:10], line[10:].strip()])
	else:
		lines.append(['          ', line.strip()])
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
	'INRIA', '-----', '=====', 'Organization', 'Netherlands', 'McGill',
	'IBM', 'CWI', 'PathBridge', 'Simula', 'Tokyo', 'Nara', 'Osaka', 'Kyushu',
	'Centrum voor Wiskunde en Informatica', 'Centrum Wiskunde & Informatica',
	'The Netherlands', 'Faculty', 'TU Delft',
	'Interactive Software Development', 'Kruislaan', 'NL-1098', 'Smetanova',
	'Slovenia', 'http://' \
)
BLANK = '          '
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
		status, mode = BLANK, 'ProgramCh'
	elif match(line, 'Advisory Committee'):
		status, mode = BLANK, 'AdviceCo'
	elif matchs(line, ('Publicity chair', 'Publicity-chair', 'Publicity Co-Chairs')) \
		and not match(line, 'Publicity chair, '):
		status, mode = BLANK, 'PubRelCh'
	elif matchs(line, ('Local organization chair', 'Local arrangements and registration',\
		'Local Co-chairs', 'Local Arrangement Chair', 'Local Organizing Chair',\
		'Local Facilities Chairs', 'Local Chair', 'Local Organisation Chair',\
		'Social Event Co-Chairs', 'Registration Co-Chairs', 'Local Arrangement Co-Chairs')):
		status, mode = BLANK, 'LocRegCh'
	elif matchs(line, ('Local Organizing Team', 'Local Arrangements')):
		status, mode = BLANK, 'LocRegCo'
	elif matchs(line, ('Panel organization chair', 'Panel Co-chairs',\
		'Panel Chair')):
		status, mode = BLANK, 'PanelCh'
	elif matchs(line, ('Post-Doctoral Symposium Co-Chairs',)):
		status, mode = BLANK, 'PodSymCh'
	elif matchs(line, ('DOCTORAL SYMPOSIUM CHAIR',\
		'Doctoral Symposium Co-Chairs', 'Doctoral Symposium Track Co-chairs')):
		status, mode = BLANK, 'DocSymCh'
	elif matchs(line, ('Student volunteers coordinator', 'Student Staff Chair',\
		'Student-volunteer Chair', 'Student Volunteers Chairs',\
		'Student Volunteers Chair', 'Student Volunteers Co-Chairs')):
		status, mode = BLANK, 'StudentCh'
	elif matchs(line, ('MIP Award Chair',)):
		status, mode = BLANK, 'AwardCh'
	elif match(line, 'Student Research Competition Chair'):
		status, mode = BLANK, 'StudComCh'
	elif matchs(line, ('Finance Co-chairs', 'Liaison Chairs - Finances',\
		'Financial Chairs', 'Finance Chair', 'Finances Chair',\
		'Finance and Registration Chair')):
		status, mode = BLANK, 'FinanceCh'
	elif matchs(line, ('ERA Track Co-chairs', 'ERA Chairs', 'ERA Co-Chairs',\
		'ERA Track Chairs')):
		status, mode = BLANK, 'EarlyCh'
	elif matchs(line, ('ERA Track Committee',)):
		status, mode = BLANK, 'EarlyCo'
	elif match(line, 'Challenge Chair'):
		status, mode = BLANK, 'ChalngCh'
	elif match(line, 'Hackathon Chair'):
		status, mode = BLANK, 'HackCh'
	elif matchs(line, ('Tutorials Co-chairs', 'Tutorial Co-Chairs',\
		'Tutorial Chairs', 'Tutorials Chair', 'Tutorial Chair')):
		status, mode = BLANK, 'TutorCh'
	elif matchs(line, ('Data Chair', 'Chief of Data')):
		status, mode = BLANK, 'DataCh'
	elif match(line, 'Satellite Events'):
		status, mode = BLANK, 'SatellCh'
	elif match(line, 'Vision Papers'):
		status, mode = BLANK, 'VisionCh'
	elif match(line, 'Project Track'):
		status, mode = BLANK, 'ProjectCh'
	elif matchs(line, ('Poster Chairs', 'Poster Chair', 'Poster Co-Chairs')):
		status, mode = BLANK, 'PosterCh'
	elif matchs(line, ('Proceedings Chair', 'Proceedings Co-chairs',\
		'Liaison Chairs - Publications', 'Publication Chair',\
		'Publications Chair')):
		status, mode = BLANK, 'PublicaCh' # == Publication Chair
	elif matchs(line, ('Invited Speaker', 'Keynote Speaker', 'Keynotes',\
		'Keynote Talks')):
		status, mode = BLANK, 'KeyNote'
	elif match(line, 'Important Dates'):
		status, mode = BLANK, BLANK
	elif matchs(line, ('Mobile Chair', 'Mobile Web Chair')):
		status, mode = BLANK, 'MobileCh'
	elif match(line, 'Expert Review Panel'):
		status, mode = BLANK, 'ExpertRP'
	elif matchs(line, ('Tool Demonstrations Program Committee',\
		'Tool track program committee')):
		status, mode = BLANK, 'DemoCo'
	elif matchs(line, ('Tool Demonstrations Chairs', 'Demonstrations Chair',\
		'Demonstrations Chairs', 'Demonstration Chairs',\
		'Tool Demonstration Co-Chairs', 'Tool Demo Co-Chairs',\
		'Tool Demonstrations Track Chairs', 'Tools Track Co-chair',\
		'Exhibition and Demo Chair')):
		status, mode = BLANK, 'DemoCh'
	elif matchs(line, ('Industry track program committee', 'Applications Track')):
		status, mode = BLANK, 'PractCo'
	elif matchs(line, ('Industry Track', 'Industrial Track Co-chair',\
		'Industry Liaison', 'Industrial Liaison Chair')):
		status, mode = BLANK, 'PractCh'
	elif match(line, 'Scientific Liason'):
		status, mode = BLANK, 'ScientLi'
	elif matchs(line, ('Program committee', 'PROGRAM COMITTEE', 'Programme Committee', \
		'Foundations Track')):
		status, mode = BLANK, 'ProgramCo'
	elif match(line, 'Program Board'):
		status, mode = BLANK, 'ProgBoCo'
	elif match(line, 'Scientific committee'):
		status, mode = BLANK, 'ScienceCo'
	elif match(line, 'Steering Committee Chair'):
		status, mode = BLANK, 'SteerCh'
	elif match(line, 'Steering committee'):
		status, mode = BLANK, 'SteerCo'
	elif match(line, 'Challenge Committee'):
		status, mode = BLANK, 'ChalngCo'
	elif match(line, 'Sponsor Chairs'):
		status, mode = BLANK, 'SponsorCh'
	elif matchs(line, ('Social media-chair', 'Social Chair', 'Social Media Chairs', 'Social Media Chair')):
		status, mode = BLANK, 'SocMedCh'
	elif matchs(line, ('Workshop organization chair', 'Workshop co-Chairs',\
		'Workshops Co-chair', 'Workshops', 'Workshop Chairs')):
		status, mode = BLANK, 'WorkspCh'
	elif matchs(line, ('General chair', 'Conference chair')):
		status, mode = BLANK, 'GeneralCh'
		# TODO: do we really care to distinguish GeCh from OrCh?
	elif match(line, 'Organization Chair'):
		status, mode = BLANK, 'OrganCh'
	elif matchs(line, ('ORGANIZATION COMMITTEE', 'organizing committee',\
		'Organizers', 'Organisation Committee', 'Organizing & Steering')):
		status, mode = BLANK, 'OrganCo'
	elif matchs(line, ('Website administration', 'Web Chair', 'Webmaster', 'Web Co-Chairs')):
		status, mode = BLANK, 'WebCh'
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
			status = 'GeneralCh'
		elif match(line, '(Finance Chair)'):
			status = 'FinanceCh'
		elif match(line, '(Challenge Chair)'):
			status = 'ChalngCh'
		elif matchs(line, ('Publicity Chair, ', ' - Publicity Chair', \
			'(Publicity co-Chair)', '(Publicity Chair)')):
			status = 'PubRelCh'
		elif match(line, '(Workshop Selection Chair)'):
			status = 'SatellCh' # NB!
		elif matchs(line, ('(Program Chair)', '(Program co-Chair)', '- Program Chair')):
			status = 'ProgramCh'
		elif matchs(line, ('(Organizing Chair)', '- Organization Chair')):
			status = 'OrganCh'
		elif match(line, '(Tutorials Chair)'):
			status = 'TutorCh'
		elif match(line, '- Briefings Chair'):
			status = 'BriefCh'
		elif match(line, '- Industry Chair'):
			status = 'PractCh'
		elif matchs(line, ('(Web Chair)', '(Web and Publicity co-Chair)', '(web)')):
			status = 'WebCh '
		elif match(line, '(social media)'):
			status = 'SocMedCh'
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
f.write('##########\n')
for status, line in lines:
	while len(status)<10:
		status += ' '
	f.write(status+line+'\n')
f.close()
