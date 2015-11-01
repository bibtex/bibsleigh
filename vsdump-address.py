#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for deriving location values from the DBLP XML dump

import sys, os.path, json
import xml.etree.cElementTree as ET
from fancy.ANSI import C
from fancy.Countries import *
from lib.AST import Sleigh
from lib.JSON import parseJSON
# from lib.NLP import nrs, strictstrip

ienputdir = '../json'
n2f_name = '_name2file.json'
name2file = parseJSON(n2f_name) if os.path.exists(n2f_name) else {}
sleigh = Sleigh(ienputdir + '/corpus', name2file)
verbose = False
procs = {}

def findOneIn(tries, arr):
	for t in tries:
		if t in arr:
			return t
	return None

def checkon(fn, o):
	if 'dblpkey' not in o.json.keys():
		print('[ {} ] {}'.format(C.red('DONT'), 'DBLP key not found on the entry'))
		return 1
	mykey = o.get('dblpkey')
	# for the rare case of multiple dblpkeys
	# (can happen as a DBLP error or when same proceedings span over multiple volumes)
	if isinstance(mykey, list):
		mykey = mykey[0]
	if mykey not in procs.keys():
		print('[ {} ] {}'.format(C.red('DONT'), 'DBLP key not found in the dump'))
		return 1
	title = procs[mykey]
	if title.endswith('.'):
		title = title[:-1]
	ws = title.replace(' - ', ', ').replace(' (', ', ').split(', ')
	country = findOneIn(knownCountries, ws)
	state = findOneIn(usaStateNames, ws)
	found = False
	if country:
		town = ws[ws.index(country)-1]
		state = '?'
		# what if "town" is an USA state? (full)
		if country == 'USA' and town in usaStateNames:
			state = town
			town = ws[ws.index(town)-1]
		# what if "town" is an USA state? (abbreviated)
		if country == 'USA' and town in usaStateAB:
			state = usaStateNames[usaStateAB.index(town)]
			town = ws[ws.index(town)-1]
		# what if "town" is a Canadian state? (full)
		if country == 'Canada' and town in canStateNames:
			state = town
			town = ws[ws.index(town)-1]
		# what if "town" is a Canadian state? (abbreviated)
		if country == 'Canada' and town in canStateAB:
			state = canStateNames[canStateAB.index(town)]
			town = ws[ws.index(town)-1]
		# the same can happen in the UK
		if country in ('UK', 'United Kingdom') and town in ('Scotland', 'Scottland'):
			state = town
			town = ws[ws.index(town)-1]
		# Georgia the country vs Georgia the state
		if country == 'Georgia' and town == 'Atlanta':
			state = country
			country = 'USA'
		# near Something
		if town.startswith('near '):
			town = ws[ws.index(town)-1]
		# Luxembourg, Luxembourg
		if country == 'Luxembourg':
			town = 'Luxembourg'
		# Saint-Malo / St. Malo
		if country == 'France' and town == 'St. Malo':
			town = 'Saint-Malo'
		# Florence / Firenze
		if country == 'Italy' and town.find('Firenze') > -1:
			town = 'Florence'
		found = True
	elif state:
		country = 'USA'
		town = ws[ws.index(state)-1]
		found = True
	else:
		# desperate times
		for sol in desperateSolutions.keys():
			if sol in ws:
				town, state, country = desperateSolutions[sol]
				found = True
	# normalise
	if country in countryMap.keys():
		country = countryMap[country]
	if country == 'United Kingdom' and state == '?':
		if town.endswith('London') or town in ('Birmingham', 'York',\
		'Coventry', 'Nottingham', 'Lancaster', 'Oxford', 'Manchester',\
		'Southampton', 'Norwich', 'Leicester', 'Canterbury'):
			state = 'England'
		elif town in ('Edinburgh', 'Glasgow'):
			state = 'Scotland'
	# report
	if 'address' in o.json.keys():
		print('[ {} ] {}'.format(C.blue('OLDA'), o.get('address')))
	if 'location' in o.json.keys():
		print('[ {} ] {}'.format(C.blue('OLDL'), o.get('location')))
	if found:
		# print('[ {} ] {}'.format(C.blue('KNOW'), country))
		print('[ {} ] {}'.format(C.blue('AD||'), title))
		print('[ {} ] {:30} || {:30} || {:20}'.format(C.blue('AD->'), C.yellow(town), C.yellow(state), C.yellow(country)))
		# TODO: perhaps later we can act more aggressively
		newaddr = [town, '' if state=='?' else state, country]
		if 'address' not in o.json.keys() or newaddr != o.json['address']:
			o.json['address'] = newaddr
			f = open(o.json['FILE'], 'w')
			f.write(o.getJSON())
			f.close()
			return 2
		# nothing changed
		return 0
	print('[ {} ] {}'.format(C.yellow('AD??'), title))
	return 1

def checkreport(fn, o):
	statuses = (C.blue('PASS'), C.red('FAIL'), C.yellow('FIXD'))
	r = checkon(fn, o)
	# non-verbose mode by default
	if verbose or r != 0:
		print('[ {} ] {}'.format(statuses[r], fn))
	return r

if __name__ == "__main__":
	if len(sys.argv) > 1:
		verbose = sys.argv[1] == '-v'
	print('{}: {} venues, {} papers\n{}'.format(\
		C.purple('BibSLEIGH'),
		C.red(len(sleigh.venues)),
		C.red(sleigh.numOfPapers()),
		C.purple('='*42)))
	cx = {0: 0, 1: 0, 2: 0}
	# now read in the proceedings entries from the dump
	if os.path.exists('_procs.json'):
		procs = json.load(open('_procs.json', 'r'))
	else:
		parser = ET.XMLParser(encoding="utf-8")
		for event, elem in ET.iterparse('../dblp.xml', events=("end",), parser=parser):
			if elem.tag == 'proceedings':
				dblpkey = elem.attrib['key']
				title = elem.findtext('title')
				procs[dblpkey] = title
		f = open('_procs.json', 'w', encoding='utf8')
		f.write(json.dumps(procs, sort_keys=True, separators=(',\n\t', ': '), ensure_ascii=False))
		f.close()
	print('{} proceedings volumes found.'.format(len(procs)))
	for v in sleigh.venues:
		for c in v.getConfs():
			cx[checkreport(c.filename, c)] += 1
	print('{} files checked, {} ok, {} fixed, {} failed'.format(\
		C.bold(cx[0] + cx[1] + cx[2]),
		C.blue(cx[0]),
		C.yellow(cx[2]),
		C.red(cx[1])))
