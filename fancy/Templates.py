#!/c/Users/vadim/AppData/Local/Programs/Python/Python37-32/python
# -*- coding: utf-8 -*-
#
# a module with hypertextual templates

# https://www.google.com/fonts#UsePlace:use/Collection:Exo+2
header = '''<!DOCTYPE html>
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
	<meta name="keywords" content="software linguistics, software language engineering, book of knowledge, glossary, academic publications, scientific research, open knowledge, open science"/>
	<title>BibSLEIGH — {title}</title>
	<link href="stuff/bib.css" rel="stylesheet" type="text/css"/>
	<link href='http://fonts.googleapis.com/css?family=Exo+2:400,700,400italic,700italic' rel='stylesheet' type='text/css'>
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

editLink = '<br/>\n<a href="{edit}"><img src="stuff/edit.png" alt="EDIT!" title="EDIT!"/></a>'
editCorpus = 'https://github.com/slebok/bibsleigh/edit/master/corpus/{filename}'
editTag = 'https://github.com/slebok/bibsleigh/edit/master/tags/{etag}.json'
editBundle = 'https://github.com/slebok/bibsleigh/edit/master/bundles/{ebundle}.json'
editPerson = 'https://github.com/slebok/bibsleigh/edit/master/people/{eperson}.json'

leftLinksT = '''
	<div class="pad">
		<a href="index.html"><img src="stuff/{statusC}-corpus.png" alt="BibSLEIGH corpus" title="All papers in the corpus"/></a><br/>
		<a href="tag/index.html"><img src="stuff/{statusT}-tags.png" alt="BibSLEIGH tags" title="All known tags"/></a><br/>
		<a href="bundle/index.html"><img src="stuff/{statusB}-bundles.png" alt="BibSLEIGH bundles" title="All selected bundles"/></a><br/>
		<a href="person/index.html"><img src="stuff/{statusP}-people.png" alt="BibSLEIGH people" title="All contributors"/></a>{elink}
	</div>
	<a href="http://creativecommons.org/licenses/by/4.0/" title="CC-BY"><img src="stuff/cc-by.png" alt="CC-BY"/></a><br/>
	<a href="http://opendatacommons.org/licenses/by/summary/" title="Open Knowledge"><img src="stuff/open-knowledge.png" alt="Open Knowledge" /></a><br/>
	<a href="http://validator.w3.org/check/referer" title="XHTML 1.0 W3C Rec"><img src="stuff/xhtml.png" alt="XHTML 1.0 W3C Rec" /></a><br/>
	<a href="http://jigsaw.w3.org/css-validator/check/referer" title="CSS 2.1 W3C CanRec"><img src="stuff/css.png" alt="CSS 2.1 W3C CanRec" class="pad" /></a><br/>
	<div class="sm">
		<a href="mailto:vadim@grammarware.net"><img src="stuff/email.png" alt="email" title="Complain!" /></a>
		<a href="https://twitter.com/intent/tweet?screen_name=grammarware"><img src="stuff/twitter.png" alt="twitter" title="Mention!" /></a>
	</div>
'''

def leftLinks(stat, edit):
	return leftLinksT.format(\
		statusC=stat[0],
		statusT=stat[1],
		statusB=stat[2],
		statusP=stat[3],
		elink=edit)

uberHTML = \
header.format(title='Bibliography of Software Language Engineering in Generated Hypertext')+\
'<a href="index.html"><img src="stuff/bibsleigh.png" alt="BibSLEIGH" title="BibSLEIGH" class="pad"/></a><br/>'+\
leftLinks('appp', '')+'''
</div>
<div class="main">
<div class="txt">
<h2>Bibliography of Software Language Engineering in Generated Hypertext (BibSLEIGH)</h2>
<p>work in progress</p></div>
<div class="txt">
<p>Facilitated browsing of scientific knowledge in and beyond software (language) engineering.<br/>
<a href="about.html">Read more about this</a>.</p>
<p>	<strong>{cxDom}</strong> domains,
	<strong>{cxVen}</strong> brands,
	<strong>{cxVol}</strong> issues,
	<strong>{cxPap}</strong> papers,
	<strong>634</strong> tags,
	<strong>324858</strong> markings.</p></div>
{items}
'''+footer

aboutHTML = \
header.format(title='Bibliography of Software Language Engineering in Generated Hypertext — About')+\
'<a href="index.html"><img src="stuff/bibsleigh.png" alt="BibSLEIGH" title="BibSLEIGH" class="pad"/></a><br/>'+\
leftLinks('pppp', '')+'''
</div>
<div class="main">
<h2>Bibliography of Software Language Engineering in Generated Hypertext (BibSLEIGH)</h2>
<p>This is a project on facilitated browsing of scientific knowledge objects in software language engineering, bridging to other domains of software engineering, computer science and artificial intelligence. It is a work in progress.</p>
<p>The following {} logos were recreated <a href="http://grammarware.net">by me</a> to represent venues.
Most follow the original designs by the conference founders/organisers,
but the original images were never used directly.
Others were improvised to create a matching feel.</p>
<p>No legal or artistic rights claimed. A couple of times public domain
images were used to aid the drawing process. If you are an organiser of
a venue and would like to get my SVG originals, feel free to send an email.</p>
{}
<br clear="both"/>
<p><a href="sync.html">Next conferences to import</a></p>
'''+footer

syncHTML = \
header.format(title='Bibliography of Software Language Engineering in Generated Hypertext — Sync')+\
'<a href="index.html"><img src="stuff/bibsleigh.png" alt="BibSLEIGH" title="BibSLEIGH" class="pad"/></a><br/>'+\
leftLinks('pppp', '')+'''
</div>
<div class="main">
<h2>Bibliography of Software Language Engineering in Generated Hypertext (BibSLEIGH)</h2>
<p>BibSLEIGH is being synced by manual executions of automated update scripts. This page is meant for the maintainer of the project to keep track of the progress.</p>
{}
'''+footer

confHTML = header+'''
	<a href="index.html"><img src="stuff/{img}.png" alt="{title}" title="{title}" class="pad"/></a>
'''+leftLinks('appp', editLink).format(edit=editCorpus)+'''
</div>
<div class="main">
<h2>{fname}</h2>{venpage}
<h3>{cxBrands} brands:</h3>
<div class="minibar">{brands}<br style="clear:left"/></div>
<h3>{cxPapers} papers in {cxIssues} issues:</h3>
<dl>{dl}</dl>
'''+footer

brandHTML = header+'''
	<a href="index.html"><img src="stuff/{img}.png" alt="{title}" title="{title}" class="pad"/></a>
'''+leftLinks('appp', editLink).format(edit=editCorpus)+'''
</div>
<div class="main">
<h2>{fname}</h2>
<h3>(brand of <a href="{parent}.html">{parent}</a>)</h2>{venpage}
<h3>{cxPapers} papers in {cxIssues} issues:</h3>
<dl>{dl}</dl>
'''+footer

def movein(s):
	return s.replace('stuff/', '../stuff/').replace('href="', 'href="../').replace('href="../http', 'href="http')

taglistHTML = header.replace('stuff/', '../stuff/')+'''
	<a href="../index.html"><img src="../stuff/bibsleigh.png" alt="BibSLEIGH" title="BibSLEIGH" class="pad"/></a>
'''+movein(leftLinks('papp', ''))+'''
</div>
<div class="main">
<h2><span class="ttl">Tag index<sup><a href="untagged.html">†</a></sup></span></h2>
<h3>{listname}:</h3>
{ul}
'''+footer

tagHTML = header.replace('stuff/', '../stuff/')+'''
	<a href="../index.html"><img src="../stuff/bibsleigh.png" alt="BibSLEIGH" title="BibSLEIGH" class="pad"/></a>
'''+movein(leftLinks('papp', editLink).format(edit=editTag))+'''
</div>
<div class="main">
<div class="tbox">
{boxlinks}
</div>
<h2><span class="ttl">Tag</span> #{tag}</h2>{above}
<h3>{listname}:</h3>
{dl}
'''+footer

wordlistHTML = header+'''
	<a href="index.html"><img src="stuff/bibsleigh.png" alt="BibSLEIGH" title="BibSLEIGH" class="pad"/></a>
'''+leftLinks('pppp', '')+'''
</div>
<div class="main">
<h2><span class="ttl">Stem index</span></h2>
<h3>{listname}:</h3>
{ul}
'''+footer

wordHTML = header.replace('stuff/', '../stuff/').replace('{title}', '{stem} stem')+'''
	<a href="../index.html"><img src="../stuff/bibsleigh.png" alt="BibSLEIGH" title="BibSLEIGH" class="pad"/></a>
'''+movein(leftLinks('pppp', ''))+'''
</div>
<div class="main">
<div class="tbox">
{inthebox}
</div>
<h2><span class="ttl">Stem</span> {stem}$ (<a href="../words.html">all stems</a>)</h2>
<h3>{listname}:</h3>
{dl}
'''+footer

peoplistHTML = header.replace('stuff/', '../stuff/')+'''
	<a href="../index.html"><img src="../stuff/bibsleigh.png" alt="BibSLEIGH" title="BibSLEIGH" class="pad"/></a>
'''+movein(leftLinks('pppa', ''))+'''
</div>
<div class="main">
<h2><span class="ttl">People index</span></h2>
<h3>{listname}:</h3>
{ul}
'''+footer

personHTML = header.replace('stuff/', '../stuff/')+'''
	<a href="../index.html"><img src="../stuff/bibsleigh.png" alt="BibSLEIGH" title="BibSLEIGH" class="pad"/></a>
'''+movein(leftLinks('pppa', editLink).format(edit=editPerson))+'''
</div>
<div class="main">{boxlinks}
<h2><span class="ttl">{gender} Person:</span> {person}</h2>
{namedlists}
'''+footer

bibHTML = header+'''
	<a href="index.html"><img src="stuff/{img}.png" alt="{title}" title="{title}" class="pad"/></a>
'''+leftLinks('appp', editLink).format(edit=editCorpus)+'''
</div>
<div class="main">
<h2>{authors}<br/><em>{stemmedTitle}</em><br/>{short}.</h2>
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

bunHTML = header.replace('stuff/', '../stuff/')+'''
	<a href="../index.html"><img src="../stuff/bibsleigh.png" alt="BibSLEIGH" title="BibSLEIGH" class="pad"/></a>
'''+movein(leftLinks('ppap', editLink).format(edit=editBundle))+'''
</div>
<div class="main">
<h2><span class="ttl">Bundle</span> {bundle}</h2>
{dl}
'''+footer

bunListHTML = header.replace('stuff/', '../stuff/')+'''
	<a href="../index.html"><img src="../stuff/bibsleigh.png" alt="BibSLEIGH" title="BibSLEIGH" class="pad"/></a>
'''+movein(leftLinks('ppap', ''))+'''
</div>
<div class="main">
<h2><span class="ttl">Bundle index</span></h2>
{ul}
'''+footer
