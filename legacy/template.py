#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

import os

header = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:xhtml="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
	<meta name="keywords" content="software linguistics, software language engineering, book of knowledge, glossary, Russian; иньекция; English; inject"/>
	<title>SLEBoK — bibSLEIGH — %s</title>
	<link href="stuff/bib.css" rel="stylesheet" type="text/css"/>
	<script src="stuff/jquery.min.js"></script>
</head>
<body>
<div class="left">'''

footer = '''
<div style="clear:both"/><hr />
<div class="last">
	<em>
		<a href="http://bibtex.github.io">Bibliography of Software Language Engineering in Generated Hypertext</a>
		(<a href="http://github.com/slebok/bibsleigh">BibSLEIGH</a>) is
		created and maintained by <a href="http://grammarware.github.io/">Dr. Vadim Zaytsev</a>.<br/>
		Hosted as a part of <a href="http://slebok.github.io/">SLEBOK</a> on <a href="http://www.github.com/">GitHub</a>.
	</em>
</div>
</body>
</html>'''

bibHTML = header+'''
	<!-- (a link to bibSLEIGH)<br/> -->
	<a href="index.html"><img src="stuff/%s.png" alt="%s" title="%s" class="pad"/></a><br/>
	<!-- (a link to edit)<br/> -->
	<a href="http://creativecommons.org/licenses/by/4.0/" title="CC-BY"><img src="stuff/cc-by.png" alt="CC-BY"/></a><br/>
	<a href="http://opendatacommons.org/licenses/by/summary/" title="Open Knowledge"><img src="stuff/open-knowledge.png" alt="Open Knowledge" class="pad" /></a><br/>
	<a href="http://validator.w3.org/check/referer" title="XHTML 1.0 W3C Rec"><img src="stuff/xhtml10.png" alt="XHTML 1.0 W3C Rec" /></a><br/>
	<a href="http://jigsaw.w3.org/css-validator/check/referer" title="CSS 2.1 W3C CanRec"><img src="stuff/css21.png" alt="CSS 2.1 W3C CanRec" class="pad" /></a><br/>
	<div>[<a href="mailto:vadim@grammarware.net">Complain!</a>]</div>
</div>
<div class="main">
<h2>
	%s<br/>
	<em>%s</em>.<br/>
	%s.
</h2>
<div class="pre">
	<form>
		<input type="checkbox" checked="true" onClick="%s"/> Full names
		<input type="checkbox" checked="true" onClick="(this.checked)?$('#doi').show():$('#doi').hide();"/> DOI
		<input type="checkbox" checked="true" onClick="(this.checked)?$('#isbn').show():$('#isbn').hide();"/> ISxN
	</form>
	<pre>%s</pre>
</div>
<hr/>
%s
'''+footer

# h.write(bibHTML %
# 	(self.getTitleTXT(),
# 	self.getVenueIcon(),
# 	self.getVenueShort(),
# 	self.getVenueShort(),
# 	self.getAuthorsHTML(),
# 	self.getTitleHTML(),
# 	self.getVenueHTML(),
# 	self.getCodeLongShort(),
# 	self.toBIB(),
# 	self.contentsHTML()))
def hyper_entry(title, vshort, authors, venue, code, bib, lst):
	if os.path.exists('../frontend2/stuff/'+vshort+'.png'):
		icon = 'stuff/'+vshort+'.png'
	else:
		# TODO: more steps back in this heuristic
		icon = 'stuff/bibsleigh.png'
	return bibHTML % (
		title.replace('<i>','').replace('</i>',''),
		icon,
		vshort,
		vshort,
		authors,
		title,
		venue,
		code,
		bib,
		lst
		)

confHTML = header.replace('%s','{title}')+'''
	<!-- (a link to bibSLEIGH)<br/> -->
	<a href="index.html"><img src="stuff/{img}.png" alt="{title}" title="{title}" class="pad"/></a><br/>
	<!-- (a link to edit)<br/> -->
	<a href="http://creativecommons.org/licenses/by/4.0/" title="CC-BY"><img src="stuff/cc-by.png" alt="CC-BY"/></a><br/>
	<a href="http://opendatacommons.org/licenses/by/summary/" title="Open Knowledge"><img src="stuff/open-knowledge.png" alt="Open Knowledge" class="pad" /></a><br/>
	<a href="http://validator.w3.org/check/referer" title="XHTML 1.0 W3C Rec"><img src="stuff/xhtml10.png" alt="XHTML 1.0 W3C Rec" /></a><br/>
	<a href="http://jigsaw.w3.org/css-validator/check/referer" title="CSS 2.1 W3C CanRec"><img src="stuff/css21.png" alt="CSS 2.1 W3C CanRec" class="pad" /></a><br/>
	<div>[<a href="mailto:vadim@grammarware.net">Complain!</a>]</div>
</div>
<div class="main">
<h2>{fname}</h2>
<h3>Editions:</h3>
<dl>{dl}</dl>
'''+footer

def hyper_series(ser, lng, eds):
	# ltitle=lng
	img = ser.lower() if os.path.exists('../frontend2/stuff/%s.png' % ser) else 'stuff/bibsleigh.png'
	return confHTML.format(title=ser, img=img, fname=('{} ({})'.format(lng, ser)), dl=''.join(eds))

uberHTML = (header % 'Bibliography of Software Language Engineering in Generated Hypertext')+'''
	<a href="index.html"><img src="stuff/bibsleigh.png" alt="BibSLEIGH" title="BibSLEIGH" class="pad"/></a><br/>
	<a href="http://creativecommons.org/licenses/by/4.0/" title="CC-BY"><img src="stuff/cc-by.png" alt="CC-BY"/></a><br/>
	<a href="http://opendatacommons.org/licenses/by/summary/" title="Open Knowledge"><img src="stuff/open-knowledge.png" alt="Open Knowledge" class="pad" /></a><br/>
	<a href="http://validator.w3.org/check/referer" title="XHTML 1.0 W3C Rec"><img src="stuff/xhtml10.png" alt="XHTML 1.0 W3C Rec" /></a><br/>
	<a href="http://jigsaw.w3.org/css-validator/check/referer" title="CSS 2.1 W3C CanRec"><img src="stuff/css21.png" alt="CSS 2.1 W3C CanRec" class="pad" /></a><br/>
	<div>[<a href="mailto:vadim@grammarware.net">Complain!</a>]</div>
</div>
<div class="main">
<h2>Bibliography of Software Language Engineering in Generated Hypertext (BibSLEIGH)</h2>
<p>Description TBD</p>
%s
'''+footer