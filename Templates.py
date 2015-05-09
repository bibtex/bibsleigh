#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

header = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:xhtml="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
	<meta name="keywords" content="software linguistics, software language engineering, book of knowledge, glossary, Russian; иньекция; English; inject"/>
	<title>SLEBoK — bibSLEIGH — {title}</title>
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

licenses = '''
	<a href="http://creativecommons.org/licenses/by/4.0/" title="CC-BY"><img src="stuff/cc-by.png" alt="CC-BY"/></a><br/>
	<a href="http://opendatacommons.org/licenses/by/summary/" title="Open Knowledge"><img src="stuff/open-knowledge.png" alt="Open Knowledge" /></a><br/>
	<a href="http://validator.w3.org/check/referer" title="XHTML 1.0 W3C Rec"><img src="stuff/xhtml.png" alt="XHTML 1.0 W3C Rec" /></a><br/>
	<a href="http://jigsaw.w3.org/css-validator/check/referer" title="CSS 2.1 W3C CanRec"><img src="stuff/css.png" alt="CSS 2.1 W3C CanRec" class="pad" /></a><br/>
	<div>[<a href="mailto:vadim@grammarware.net">Complain!</a>]</div>
'''

uberHTML = \
header.format(title='Bibliography of Software Language Engineering in Generated Hypertext')+\
'<a href="index.html"><img src="stuff/bibsleigh.png" alt="BibSLEIGH" title="BibSLEIGH" class="pad"/></a><br/>'+\
licenses+'''
</div>
<div class="main">
<h2>Bibliography of Software Language Engineering in Generated Hypertext (BibSLEIGH)</h2>
<p>Work in progress!</p>
{}
'''+footer

confHTML = header+'''
	<!-- (a link to bibSLEIGH)<br/> -->
	<a href="index.html"><img src="stuff/{img}.png" alt="{title}" title="{title}" class="pad"/></a><br/>
	<!-- (a link to edit)<br/> -->'''+licenses+'''
</div>
<div class="main">
<h2>{fname}</h2>
<h3>Editions:</h3>
<dl>{dl}</dl>
'''+footer

bibHTML = header+'''
	<!-- (a link to bibSLEIGH)<br/> -->
	<a href="index.html"><img src="stuff/{img}.png" alt="{title}" title="{title}" class="pad"/></a><br/>
	<!-- (a link to edit)<br/> -->'''+licenses+'''
</div>
<div class="main">
<h2>{authors}<br/><em>{title}</em>.<br/>{short}.</h2>
<div class="pre">
	<form>
		<input type="checkbox" checked="true" onClick="{code}"/> Full names
		<input type="checkbox" checked="true" onClick="(this.checked)?$('#uri').show():$('#uri').hide();"/> Links
		<input type="checkbox" checked="true" onClick="(this.checked)?$('#isbn').show():$('#isbn').hide();"/> ISxN
	</form>
	<pre>{bib}</pre>
</div>
<hr/>
{contents}
'''+footer
