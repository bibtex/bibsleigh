#!/usr/local/bin/python3

f = open('venues.unq','r')
g = open('venues.lst','w')
for line in f.readlines():
	line = line.strip().replace("'","\\'")
	g.write("'%s':\n\t'%s',\n" % (line, line.split('(')[0].strip()))
f.close()
g.close()
