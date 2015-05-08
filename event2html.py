#!/usr/local/bin/python3

import os, sys, glob
from template import uberHTML, confHTML, bibHTML, hyper_series
from supported import supported

def last(x):
	return x.split('/')[-1].replace('.json','')

'''
{
	"type": "inproceedings",
	"dblpkey": "conf/gttse/AndradeGAEK06",
	"venue": "GTTSE",
	"author": ["Luis Filipe Andrade", "João Gouveia", "Miguel Antunes", "Mohammad El-Ramly", "Georgios Koutsoukos"],
	"title": "Forms2Net - Migrating Oracle Forms to Microsoft .NET",
	"booktitle": "Revised Papers of the First International Summer School on Generative and Transformational Techniques in Software Engineering",
	"booktitleshort": "GTTSE",
	"year": 2005,
	"editor": ["Ralf Lämmel", "João Saraiva", "Joost Visser"],
	"pages": "261--277",
	"crossref": "conf/gttse/2006",
	"ee": "http://dx.doi.org/10.1007/11877028_8",
	"doi": "10.1007/11877028_8",
	"publisher": "Springer",
	"isbn": "3-540-45778-X",
	"volume": "4143",
	"series": "Lecture Notes in Computer Science",
	"seriesshort": "LNCS"
}
'''
def parseJSON(fn):
	dct = {}
	f = open(fn,'r')
	for line in f.readlines():
		line = line.strip()
		if line in ('{','}',''):
			continue
		perq = line.split('"')
		if len(perq) == 5:
			dct[perq[1]] = perq[3]
		elif len(perq) == 3 and perq[1] == 'year':
			dct[perq[1]] = int(perq[-1][2:-1])
		elif len(perq) > 5:
			dct[perq[1]] = list(filter(lambda x: x != ', ',perq[3:-1]))
		else:
			print('Skipped line',line,'in',fn)
	f.close()
	dct['FILE'] = fn
	return dct

# works on editions
def getAllOfType(t,dct):
	return [dct[k] for k in dct.keys() if "type" in dct[k].keys() and dct[k]["type"]==t]
# works on series
def getAllOfTypeS(t,dct):
	return [dct[k][j] for k in dct.keys() for j in dct[k].keys() if "type" in dct[k][j].keys() and dct[k][j]["type"]==t]

def json2bib(d):
	s = '@%s{%s,\n' % (d['type'], d['FILE'].split('/')[-1].replace('.json',''))
	for k in d.keys():
		if k == k.upper():
			# secret key
			continue
		if k in ('author', 'editor'):
			s += '\t%-10s = "%s",\n' % (k,' and '.join(d[k]))
		elif k in ('title', 'booktitle', 'series', 'publisher'):
			if len(d[k])==1:
				s += '\t%-10s = "{%s}",\n' % (k,d[k])
			else:
				s += '\t%-10s = "{<span id="%s">%s</span>}",\n' % (k,k,d[k])
		elif k in ('ee','crossref','key'):
			pass
		elif k == 'doi':
			s += '<span id="doi">\t%-10s = "<a href="http://dx.doi.org/%s">%s</a>",\n</span>' % (k,d[k],d[k])
		elif k == 'isbn':
			s += '<span id="isbn">\t%-10s = "%s",\n</span>' % (k,d[k])
		else:
			s += '\t%-10s = "%s",\n' % (k,d[k])
	s += '}'
	return s.replace('<i>','\\emph{').replace('</i>','}')

def json2authors(d):
	if 'author' in d.keys() and d['author']:
		return ', '.join(d['author'])
	elif 'editor' in d.keys() and d['editor']:
		return ', '.join(d['editor'])+' (editors)'
	else:
		print('ERROR: neither authors nor editor in', d)
		return ''

def json2codelong(d):
	code = ''
	for tag in ('title', 'booktitle', 'series', 'publisher'):
		if tag in d.keys() and len(d[tag]) == 2:
			code += "$('#"+tag+"').text(this.checked?'%s':'%s');" % tuple(d[tag])
	return code

def json2html(d):
	if 'booktitle' in d.keys() and d['booktitle']:
		if d['booktitle'][-1] in supported.keys():
			vshort = supported[d['booktitle'][-1]]
		else:
			vshort = '%s, %s' % (d['booktitle'], d['year'])
	else:
		vshort = '???, %s' % d['year']
	return bibHTML % \
		(
			d['title'].replace('<i>', '').replace('</i>', ''),
			d['booktitle'].lower() if 'booktitle' in d.keys() else '',
			vshort,
			vshort,
			json2authors(d),
			d['title'],
			'%s, %s' % (d['booktitle'], d['year']) if 'booktitle' in d.keys() else '',
			json2codelong(d),
			json2bib(d),
			'NOT GENERATED' #self.contentsHTML())
		)

if __name__ == "__main__":
	GCX = 0
	allconfs = []
	for top in glob.glob('bibdata/*'):
		conf = last(top)
		print('%s conference found' % conf)
		allconfs.append(conf)
		ocx = 0
		gcx = 0
		eds = {}
		for run in glob.glob(top + '/*'):
			eddict = {}
			if not os.path.isdir(run):
				ocx += 1
				continue
			cx = 0
			for pub in glob.glob(run + '/*.json'):
				cx += 1
				gcx += 1
				eddict[last(pub)] = parseJSON(pub)
			procs = {}
			for json in getAllOfType('proceedings', eddict):
				# print('Candidate name:',json['title'])
				procs[json['title']] = last(json['FILE'])
				if json['year'] not in eds.keys():
					eds[json['year']] = []
				eds[json['year']].append('<a href="%s.html">%s</a> (%s)' % (last(json['FILE']),json['title'],last(json['FILE']).replace('-',' ') ))
			for json in getAllOfType('inproceedings', eddict):
				if json['booktitle'] in procs.keys():
					pass
				else:
					print('	(Unexpected name: %s)'%json['booktitle'])
					procs[json['booktitle']] = ''
					if json['year'] not in eds.keys():
						eds[json['year']] = []
					eds[json['year']].append(json['booktitle'])
			for tit in procs.keys():
				if not procs[tit]:
					print('		Orphaned all papers of ', tit)
					continue
				f = open('../frontend2/'+procs[tit]+'.html', 'w')
				# f.write('NOT GENERATED of %s | %s | %s' % (tit, procs[tit], eddict[procs[tit]]))
				f.write(json2html(eddict[procs[tit]]))
				# cname = '%s (%s)' % (self.sup, self.ven)
				# f.write(confHTML.format(img=self.ven.lower(), title=self.sup, fname=cname, dl=ven.getHTML()))
				f.close()
			# for k in eds.keys():
			# 	eds[k] = '\n'.join(['<dd>%s</dd>' % e for e in eds[k]])
			print('	%s: %s papers' % (last(run),cx))
			# f = open('frontend2/'+conf.lower()+'/'+last(run)+'.html','w')
			# f.write(confHTML % (
			# 	conf,
			# 	conf.lower(),
			# 	conf,
			# 	conf,
			# 	'%s (%s)' % ('Full venue name', conf),
			# 	'papers be here'))
			# f.close()
		f = open('../frontend2/'+conf+'.html', 'w')
		f.write(hyper_series(conf,supported[conf],
			'\n'.join(['<dt>%s</dt>%s' % (y,'\n'.join(['<dd>%s</dd>' % e for e in eds[y]])) for y in reversed(sorted(eds.keys()))])
		))
		f.close()
		if ocx:
			print('	[%s orphans]' % ocx)
		if gcx:
			print('	[%s papers total]' % gcx)
			GCX += gcx
	if GCX:
		print('[%s papers total]' % GCX)
	f = open('../frontend2/index.html', 'w')
	f.write(uberHTML % '\n'.join([
		'<div class="pic"><a href="%s.html" title="%l"><img src="stuff/%s.png" alt="%s"><br/>%s</a></div>'.replace('%s',conf).replace('%l',supported[conf])
		for conf in allconfs]))
	f.close()
	sys.exit(0)
