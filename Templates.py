#!/usr/local/bin/python3
# -*- coding: utf-8 -*-

header = '''<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
	<meta name="keywords" content="software linguistics, software language engineering, book of knowledge, glossary, Russian; иньекция; English; inject"/>
	<title>SLEBoK — bibSLEIGH — {title}</title>
	<link href="stuff/bib.css" rel="stylesheet" type="text/css"/>
	<script src="stuff/jquery.min.js" type="text/javascript"></script>
</head>
<body>
<div class="left">'''

footer = '''</div>
<hr style="clear:both"/>
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
'''<a href="index.html"><img src="stuff/bibsleigh.png" alt="BibSLEIGH" title="BibSLEIGH" class="pad"/></a><br/>
   <div class="pad"><a href="tag/index.html">Tag index</a></div><br/>'''+\
licenses+'''
</div>
<div class="main">
<h2>Bibliography of Software Language Engineering in Generated Hypertext (BibSLEIGH)</h2>
<p>Work in progress! <strong>{}</strong> venues and <strong>{}</strong> papers currently in the database.</p>
{}
'''+footer

confHTML = header+'''
	<!-- (a link to bibSLEIGH)<br/> -->
	<a href="index.html"><img src="stuff/{img}.png" alt="{title}" title="{title}" class="pad"/></a><br/>
	<div class="pad"><a href="https://github.com/slebok/bibsleigh/tree/master/{filename}">EDIT</a></div><br/>
'''+licenses+'''
</div>
<div class="main">
<h2>{fname}</h2>
<h3>Editions:</h3>
<dl>{dl}</dl>
'''+footer

taglistHTML = header.replace('stuff/', '../stuff/')+'''
	<!-- (a link to bibSLEIGH)<br/> -->
	<a href="../index.html"><img src="../stuff/bibsleigh.png" alt="BibSLEIGH" title="BibSLEIGH" class="pad"/></a><br/>
	<div class="pad"><a href="index.html">Tag index</a></div><br/>
'''+licenses.replace('stuff/', '../stuff/')+'''
</div>
<div class="main">
<h2><span class="ttl">Tag index</span></h2>
<h3>{listname}:</h3>
{dl}
'''+footer

tagHTML = header.replace('stuff/', '../stuff/')+'''
	<!-- (a link to bibSLEIGH)<br/> -->
	<a href="../index.html"><img src="../stuff/bibsleigh.png" alt="BibSLEIGH" title="BibSLEIGH"/></a><br/>
	<div class="pad"><a href="index.html">Tag index</a></div><br/>
	<div class="pad"><a href="https://github.com/bibtex/bibeauty/edit/master/tags/{tag}.json">EDIT</a></div><br/>
'''+licenses.replace('stuff/', '../stuff/')+'''
</div>
<div class="main">
<h2><span class="ttl">Tag</span> {tag}</h2>
<h3>{listname}:</h3>
{dl}
'''+footer

bibHTML = header+'''
	<!-- (a link to bibSLEIGH)<br/> -->
	<a href="index.html"><img src="stuff/{img}.png" alt="{title}" title="{title}" class="pad"/></a><br/>
	<div class="pad"><a href="https://github.com/slebok/bibsleigh/edit/master/{filename}">EDIT</a></div><br/>
'''+licenses+'''
</div>
<div class="main">
<h2>{authors}<br/><em>{title}</em><br/>{short}.</h2>
<div class="rbox">
{boxlinks}
</div>
<div class="pre"><form action="#">
	<input type="checkbox" checked="checked" onClick="{code}"/> Full names
	<input type="checkbox" checked="checked" onClick="(this.checked)?$('.uri').show():$('.uri').hide();"/> Links
	<input type="checkbox" checked="checked" onClick="(this.checked)?$('#isbn').show():$('#isbn').hide();"/> ISxN
	</form><pre>{bib}</pre>
</div>
<hr/>
{contents}
'''+footer
