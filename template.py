#!/usr/local/bin/python3

bibHTML = '''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:xhtml="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
	<meta name="keywords" content="software linguistics, software language engineering, book of knowledge, glossary, Russian; иньекция; English; inject"/>
	<title>SL(E)BOK — bibSLEIGH — %s</title>
	<link href="../sleg.css" rel="stylesheet" type="text/css"/>
	<script src="jquery.min.js"></script>
</head>
<body>
<div class="left">
	(a link to bibSLEIGH)<br/>
	<a href="index.html"><img src="../conf/sle.png" alt="Software Language Engineering" class="pad"/></a><br/>
	(a link to edit)<br/>
	<a href="http://creativecommons.org/licenses/by-sa/3.0/" title="CC-BY-SA"><img src="../www/cc-by-sa.png" alt="CC-BY-SA"/></a><br/>
	<a href="http://creativecommons.org/licenses/by-sa/3.0/" title="Open Knowledge"><img src="../www/open-knowledge.png" alt="Open Knowledge" class="pad" /></a><br/>
	<a href="http://validator.w3.org/check/referer" title="XHTML 1.0 W3C Rec"><img src="../www/xhtml10.png" alt="XHTML 1.0 W3C Rec" /></a><br/>
	<a href="http://jigsaw.w3.org/css-validator/check/referer" title="CSS 2.1 W3C CanRec"><img src="../www/css21.png" alt="CSS 2.1 W3C CanRec" class="pad" /></a><br/>
	<div>[<a href="mailto:vadim@grammarware.net">Complain!</a>]</div>
</div>
<div class="main">
<h2>
	%s<br/>
	<em>%s</em>.<br/>
	%s.
</h2>
<pre>%s</pre>
<div style="clear:both"/><hr />
<div class="last">
	<em>
		<a href="http://github.com/slebok/bibsleigh">Bibliography of Software Language Engineering IGH</a> (BibSLEIGH) is
		created and maintained by <a href="http://grammarware.net">Dr. Vadim Zaytsev</a>.<br/>
		Hosted as a part of <a href="http://slebok.github.io/">SLEBOK</a> on <a href="http://www.github.com/">GitHub</a>.
	</em>
</div>
</body>
</html>'''
