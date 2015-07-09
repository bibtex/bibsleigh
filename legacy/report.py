#!/usr/local/bin/python3

import os, sys, glob

def last(x):
	return x.split('/')[-1]

if __name__ == "__main__":
	GCX = 0
	for top in glob.glob('bibdata/*'):
		conf = last(top)
		print('%s conference found' % conf)
		fcx = 0
		ocx = 0
		gcx = 0
		for bib in glob.glob(top + '/*.json'):
			version = top+'/'+'-'.join(last(bib).split('-')[:2]).replace('.json','')
			if not os.path.exists(version):
				os.mkdir(version)
			os.replace(bib, version+'/'+last(bib))
			fcx += 1
		for run in glob.glob(top + '/*'):
			if not os.path.isdir(run):
				ocx += 1
				continue
			cx = 0
			for pub in glob.glob(run + '/*.json'):
				cx += 1
				gcx += 1
			print('	%s: %s papers' % (last(run),cx))
		if ocx:
			print('	[%s orphans]' % ocx)
		if fcx:
			print('	[%s fixed orphans]' % fcx)
		if gcx:
			print('	[%s papers total]' % gcx)
			GCX += gcx
	if GCX:
		print('[%s papers total]' % GCX)
	sys.exit(0)