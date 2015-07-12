#!/usr/local/bin/python3
# -*- coding: utf-8 -*-
#
# a module for renaming conferences (with papers inside)

import sys, os.path, glob
from fancy.ANSI import C
# sys.path.append(os.getcwd()+'/../engine')
# import Fancy, AST

ienputdir = '../json'
# sleigh = Sleigh(ienputdir + '/corpus')
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
	if len(sys.argv) < 2:
		print('Usage:\n\t{} [<DIR>]'.format(sys.argv[0]))
		sys.exit(1)
	name = sys.argv[1]
	verbose = sys.argv[-1] == '-v'
	namem = name.split('/')[-1]
	cx = {0: 0, 1: 0, 2: 0}
	if not os.path.exists(ienputdir + '/corpus/' + name):
		report(name, name, 1)
		sys.exit(1)
	# for all papers...
	for fn in glob.glob(ienputdir + '/corpus/' + name + '/*.json'):
		pureold = fn.split(namem+'/')[1]
		if pureold.endswith('.json'):
			pureold = pureold[:-5]
		purenew = pureold
		if purenew[-2:] == namem[-2:]:
			purenew = purenew[:-2]
		if pureold == purenew:
			cx[report(pureold, purenew, 0)] += 1
		elif not os.path.exists(ienputdir + '/corpus/' + name + '/' + pureold + '.json')\
			 and os.path.exists(ienputdir + '/corpus/' + name + '/' + purenew + '.json'):
			cx[report(pureold, purenew, 1)] += 1
		else:
			cx[report(pureold, purenew, 2)] += 1
			os.rename(ienputdir + '/corpus/' + name + '/' + pureold + '.json', \
					  ienputdir + '/corpus/' + name + '/' + purenew + '.json')
	print('{} files checked, {} ok, {} fixed, {} failed'.format(\
		C.bold(cx[0] + cx[1] + cx[2]),
		C.blue(cx[0]),
		C.yellow(cx[2]),
		C.red(cx[1])))
