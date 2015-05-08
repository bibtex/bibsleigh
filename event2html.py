#!/usr/local/bin/python3

import os, sys, glob
from template import uberHTML, confHTML, hyper_series
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
		s = '@%s{%s,\n' % (d['type'], d['FILE'].replace('.json',''))
		for k in d.keys():
			if k in ('author', 'editor'):
				s += '\t%-10s = "%s",\n' % (k,' and '.join(self.dict[k]))
			elif k in ('title', 'booktitle', 'series', 'publisher'):
				if len(self.dict[k])==1:
					s += '\t%-10s = "{%s}",\n' % (k,self.dict[k][0])
				else:
					s += '\t%-10s = "{<span id="%s">%s</span>}",\n' % (k,k,self.dict[k][0])
			elif k in ('ee','crossref','key'):
				pass
			elif k == 'doi':
				s += '<span id="doi">\t%-10s = "<a href="http://dx.doi.org/%s">%s</a>",\n</span>' % (k,self.dict[k][0],self.dict[k][0])
			elif k == 'isbn':
				s += '<span id="isbn">\t%-10s = "%s",\n</span>' % (k,self.dict[k][0])
			else:
				s += '\t%-10s = "%s",\n' % (k,self.dict[k][0])
		s += '}'
		return s.replace('<i>','\\emph{').replace('</i>','}')

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
			for json in getAllOfType('proceedings',eddict):
				# print('Candidate name:',json['title'])
				procs[json['title']] = last(json['FILE'])
				if json['year'] not in eds.keys():
					eds[json['year']] = []
				eds[json['year']].append('<a href="%s.html">%s</a> (%s)' % (last(json['FILE']),json['title'],last(json['FILE']).replace('-',' ') ))
			for json in getAllOfType('inproceedings',eddict):
				if json['booktitle'] in procs.keys():
					pass
				else:
					print('	(Unexprected name: %s)'%json['booktitle'])
					procs[json['booktitle']] = ''
					if json['year'] not in eds.keys():
						eds[json['year']] = []
					eds[json['year']].append(json['booktitle'])
			for tit in procs.keys():
				if not procs[tit]:
					print('		Orphaned all papers of ',tit)
					continue
				f = open('deploy/'+procs[tit]+'.html','w')
				f.write('NOT GENERATED')
				f.close()
			# for k in eds.keys():
			# 	eds[k] = '\n'.join(['<dd>%s</dd>' % e for e in eds[k]])
			print('	%s: %s papers' % (last(run),cx))
			# f = open('deploy/'+conf.lower()+'/'+last(run)+'.html','w')
			# f.write(confHTML % (
			# 	conf,
			# 	conf.lower(),
			# 	conf,
			# 	conf,
			# 	'%s (%s)' % ('Full venue name', conf),
			# 	'papers be here'))
			# f.close()
		f = open('deploy/'+conf+'.html','w')
		f.write(hyper_series(conf,supported[conf],
			'\n'.join(['<dt>%s</dt>%s' % (y,'\n'.join(['<dd>%s</dd>' % e for e in eds[y]])) for y in sorted(eds.keys())])
		))
		f.close()
		if ocx:
			print('	[%s orphans]' % ocx)
		if gcx:
			print('	[%s papers total]' % gcx)
			GCX += gcx
	if GCX:
		print('[%s papers total]' % GCX)
	f = open('deploy/index.html','w')
	f.write(uberHTML % '\n'.join([
		'<div class="pic"><a href="%s.html" title="%l"><img src="brand/%s.png" alt="%s"><br/>%s</a></div>'.replace('%s',conf).replace('%l',supported[conf])
		for conf in allconfs]))
	f.close()
	sys.exit(0)