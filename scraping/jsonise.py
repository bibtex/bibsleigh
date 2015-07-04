#!/usr/local/bin/python3

def js(s):
	if len(s) == 1:
		return '"{}"'.format(s[0])
	else:
		return '[' + ', '.join(['"{}"'.format(b) for b in s]) + ']'

f = open('kbse-1993.txt')
lines = f.readlines()
f.close()
i = 0
cx = 0
while i < len(lines):
	title = lines[i].strip().replace('  ', ' ')
	auths = lines[i+1].strip().split(', ')
	assert lines[i+2].strip() == ''
	cx += 1
	key = 'KBSE-1993-' + auths[0].split(' ')[-1]
	if len(auths) > 1:
		for a in auths[1:]:
			key += a.split(' ')[-1][0]
	print(key)
	f = open('KBSE-1993/'+key+'.json', 'w')
	f.write('''{{
	"venue": "ASE",
	"booktitle": "Proceedings of the 8th Annual Knowledge-Based Software Engineering Conference",
	"booktitleshort": "KBSE",
	"type": "inproceedings",
	"year": 1993,
	"title": "{}",
	"editor": ["Bruce Johnson", "Mehdi Harandi", "Bill Sasso"],
	"author": {},
	"pages": {}
}}
'''.format(title, js(auths), cx))
	f.close()
	i += 3
print(cx, 'papers processed')
