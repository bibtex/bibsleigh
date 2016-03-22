#!/c/Users/vadim/AppData/Local/Programs/Python/Python35/python
# -*- coding: utf-8 -*-
#
# a module containing a the bibtex schema
# source: https://en.wikipedia.org/wiki/BibTeX#Entry_types

# Changes:
#      + added 'publisher' to 'article'
#      + added 'journal' to 'proceedings'
#      + added 'booktitle' to 'proceedings' (SHOULD BE REMOVED LATER)
bibtex = { \
	'article': \
		({'author', 'title', 'journal', 'year', 'volume'}, \
		{'number', 'pages', 'month', 'note', 'key',
			'publisher'}), \
	'book': \
		({'author', 'editor', 'title', 'publisher', 'year'}, \
		{'volume', 'number', 'series', 'address', 'edition', 'month', 'note', 'key'}), \
	'booklet': \
		({'title'}, \
		{'author', 'howpublished', 'address', 'month', 'year', 'note', 'key'}), \
	'conference': \
		({'author', 'title', 'booktitle', 'year'}, \
		{'editor', 'volume', 'number', 'series', 'pages', 'address', 'month', 'organization', \
			'publisher', 'note', 'key'}), \
	'inbook': \
		({'author', 'editor', 'title', 'chapter', 'pages', 'publisher', 'year'}, \
		{'volume', 'number', 'series', 'type', 'address', 'edition', 'month', 'note', 'key'}), \
	'incollection': \
		({'author', 'title', 'booktitle', 'publisher', 'year'}, \
		{'editor', 'volume', 'number', 'series', 'type', 'chapter', 'pages', 'address', 'edition', \
			'month', 'note', 'key'}), \
	'inproceedings': \
		({'author', 'title', 'booktitle', 'year'}, \
		{'editor', 'volume', 'number', 'series', 'pages', 'address', 'month', 'organization', \
			'publisher', 'note', 'key'}), \
	'manual': \
		({'title'}, \
		{'author', 'organization', 'address', 'edition', 'month', 'year', 'note', 'key'}), \
	'mastersthesis': \
		({'author', 'title', 'school', 'year'}, \
		{'type', 'address', 'month', 'note', 'key'}), \
	'misc': \
		({}, \
		{'author', 'title', 'howpublished', 'month', 'year', 'note', 'key'}), \
	'phdthesis': \
		({'author', 'title', 'school', 'year'}, \
		{'type', 'address', 'month', 'note', 'key'}), \
	'proceedings': \
		({'title', 'year'}, \
		{'editor', 'volume', 'number', 'series', 'address', 'month', 'publisher', 'organization', \
			'note', 'key', 'journal', 'booktitle'}), \
	'techreport': \
		({'author', 'title', 'institution', 'year'}, \
		{'type', 'number', 'address', 'month', 'note', 'key'}), \
	'unpublished': \
		({'author', 'title', 'note'}, \
		{'month', 'year', 'key'}), \
}

sleighkeys = ('tag', 'tagged', 'stemmed', 'dblpkey', 'dblpurl', 'eventurl', 'eventtitle', \
	'roles', 'venue', 'FILE')
alwaysok = ('doi', 'acmid', 'ee', 'type', 'url', 'crossref', 'isbn')
