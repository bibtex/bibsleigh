#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import glob, os

inputdir = 'bibdata'
outputdir = '../bibtest'

def last(xx):
	return xx.split('/')[-1].replace('.json', '')

if __name__ == "__main__":
	for d in glob.glob(inputdir+'/*'):
		print('Venue', last(d))
		for c in glob.glob(d+'/*'):
			r = c+'/'+last(c)+'.json'
			y = last(c).split('-')[-1]
			td = outputdir + '/' + last(d) + '/' + y
			nr = td + '/' + last(c) + '.json'
			nc = td + '/' + last(c)
			if not os.path.exists(td):
				os.makedirs(td)
			if os.path.exists(r):
				print('{} -> {}'.format(r, nr))
				os.rename(r, nr)
			print('{}/ -> {}/'.format(c, nc))
			os.rename(c, nc)
