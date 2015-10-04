#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for scraping MGP into a CSV database

import glob, os.path

rel = []

def getints(S):
	return [int(z) for z in S.strip().split(';') if z.isdigit()]

if __name__ == "__main__":
	cx = val = unval = rel = 0
	asmt = {}
	id2name = {}
	supervisorOf = {}
	for p in glob.glob('p?'):
		fname = p+'/'+'_id2name.csv'
		fadvs = p+'/'+'_id2adv.csv'
		fkids = p+'/'+'_id2kids.csv'
		if os.path.exists(fname):
			print(fname, 'found')
			f = open(fname, 'r')
			oldline = ''
			for line in f.readlines():
				# [0]: ID
				# [1]: name
				# [2]: degree
				# [3]: book title
				# [4]: country
				# [5]: university
				# [6]: year
				if not line.strip():
					continue
				if oldline:
					line = oldline + ' ' + line
					oldline = ''
				# data = line.strip(';')
				cx += 1
				data = line.strip().split(';')
				key = tuple([x not in ('', '???') for x in data])
				if len(key) < 7:
					# if too few fields, treat as a soft line wrap
					oldline = line
					continue
				if len(key) > 7:
					# we assume that extra semicolons come from the title
					data = line.strip().split(';')
					data = data[:3] + [' '.join(data[3:-3])] + data[-3:]
					key = tuple([x not in ('', '???') for x in data])
				if len(key) != 7:
					print('Anomalous entry with', len(key), 'columns:', line)
					print(key)
				if key not in asmt.keys():
					asmt[key] = 1
				else:
					asmt[key] += 1
				if data[0] in id2name.keys():
					print('Duplicate', data[0], data[1], 'vs', id2name[data[0]])
				else:
					data[0] = int(data[0])
					id2name[data[0]] = data[1]
				if key.count(True) < 2:
					print('Sad about', data)
			f.close()
		if os.path.exists(fadvs):
			print(fadvs, 'found')
			f = open(fadvs, 'r')
			for line in f.readlines():
				kid, par = getints(line)
				if kid not in supervisorOf.keys():
					supervisorOf[kid] = []
				supervisorOf[kid].append(par)
				rel += 1
			f.close()
		if os.path.exists(fkids):
			print(fkids, 'found')
			f = open(fkids, 'r')
			for line in f.readlines():
				# year or no year
				data = getints(line)
				par, kid = data[:2]
				if kid not in supervisorOf.keys():
					supervisorOf[kid] = []
				if par in supervisorOf[kid]:
					val += 1
				else:
					supervisorOf[kid].append(par)
					unval += 1
			f.close()
	asmt[tuple([False]*7)] = max(id2name.keys())-len(id2name)
	f = open('_report1.csv', 'w')
	for k in asmt.keys():
		lst = list(k)
		lst.append(asmt[k])
		s = ';'.join([str(x) for x in lst])
		print(s)
		f.write(s+'\n')
	f.close()
	cx = sum([len(supervisorOf[y]) for y in supervisorOf.keys()])
	f = open('_report2.csv', 'w')
	f.write('relations total;{}\n'.format(cx))
	f.write('relations seen from below;{}\n'.format(rel))
	f.write('relations seen from above;{}\n'.format(unval))
	f.write('relations seen from both;{}\n'.format(val))
	f.close()
	f = open('_vis.dot', 'w')
	f.write('digraph MGP {\n')
	for k in supervisorOf.keys():
		if k not in id2name.keys():
			print('What is the name of', k)
			id2name[k] = '?{}?'.format(k)
		for sup in supervisorOf[k]:
			if sup not in id2name.keys():
				print('What is the name of', sup)
				id2name[sup] = '?{}?'.format(sup)
			f.write('\t"{}" -> "{}";\n'.format(id2name[k], id2name[sup]))
	f.write('}\n')
	f.close()
	f = open('_visy.gml', 'w')
	f.write('graph [ directed 1 id 65535\n')
	for n in id2name.keys():
		f.write('\tnode [ id {} label "{}"]\n'.format(n, id2name[n].replace('"', '')))
	for k in supervisorOf.keys():
		for sup in supervisorOf[k]:
			f.write('\tedge [ source {} target {} ]\n'.format(k, sup))
	f.write(']\n')
	f.close()
	# graph [ directed 1 id 65535
	# node [ id 1 label "new"]
