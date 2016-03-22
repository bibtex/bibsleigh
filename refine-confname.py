#!/c/Users/vadim/AppData/Local/Programs/Python/Python35/python
# -*- coding: utf-8 -*-
#
# a module for renaming conferences (with papers inside)

import sys, os.path, glob
from fancy.ANSI import C
from lib.LP import lastSlash

ienputdir = '../json'
verbose = False

def report(fn1, fn2, r):
	statuses = (C.blue(' PASS '), C.red(' FAIL '), C.yellow('RENAME'))
	# non-verbose mode by default
	if verbose or r != 0:
		print('[ {} ] {} → {}'.format(statuses[r], fn1, fn2))
	return r

if __name__ == "__main__":
	print('{} conference renamer\n{}'.format(\
		C.purple('BibSLEIGH'),
		C.purple('='*42)))
	if len(sys.argv) < 3:
		print('Usage:\n\t{} <OLD-NAME> <NEW-NAME>'.format(sys.argv[0]))
		sys.exit(1)
	nameold, namenew = sys.argv[1:3]
	verbose = sys.argv[-1] == '-v'
	nameoldm = lastSlash(nameold)
	namenewm = lastSlash(namenew)
	print(nameoldm)
	cx = {0: 0, 1: 0, 2: 0}
	if not os.path.exists(ienputdir + '/corpus/' + nameold)\
	or not os.path.isdir(ienputdir + '/corpus/' + nameold)\
	or os.path.exists(ienputdir + '/corpus/' + namenew):
		report(nameold, namenew, 1)
		sys.exit(1)
	os.makedirs(ienputdir + '/corpus/' + namenew)
	cx[report('∅', namenew, 2)] += 2
	# for all papers...
	for fn in glob.glob(ienputdir + '/corpus/' + nameold + '/*.json'):
		pureold = fn.split(nameoldm+'/')[1]
		if pureold.endswith('.json'):
			pureold = pureold[:-5]
		purenew = pureold.replace(nameoldm, namenewm)
		if purenew[-2:] == namenewm[-2:]:
			purenew = purenew[:-2]
		# print('Candidate:', pureold, 'to', purenew)
		if pureold == purenew:
			cx[report(pureold, purenew, 0)] += 1
		elif not os.path.exists(ienputdir + '/corpus/' + nameold + '/' + pureold + '.json')\
			 and os.path.exists(ienputdir + '/corpus/' + namenew + '/' + purenew + '.json'):
			cx[report(pureold, purenew, 1)] += 1
		else:
			cx[report(pureold, purenew, 2)] += 1
			os.rename(ienputdir + '/corpus/' + nameold + '/' + pureold + '.json', \
					  ienputdir + '/corpus/' + namenew + '/' + purenew + '.json')
	# now for the main file
	if not os.path.exists(ienputdir + '/corpus/' + nameold + '.json')\
	or os.path.exists(ienputdir + '/corpus/' + namenew + '.json'):
		report(nameold + '.json', namenew + '.json', 1)
		sys.exit(1)
	else:
		cx[report(nameold + '.json', namenew + '.json', 2)] += 1
		os.rename(ienputdir + '/corpus/' + nameold + '.json', \
				  ienputdir + '/corpus/' + namenew + '.json')
	try:
		os.removedirs(ienputdir + '/corpus/' + nameold)
		cx[report(nameold, '/dev/null', 2)] += 1
	except OSError:
		cx[report(nameold, '/dev/null', 1)] += 1
	print('{} files checked, {} ok, {} fixed, {} failed'.format(\
		C.bold(cx[0] + cx[1] + cx[2]),
		C.blue(cx[0]),
		C.yellow(cx[2]),
		C.red(cx[1])))
