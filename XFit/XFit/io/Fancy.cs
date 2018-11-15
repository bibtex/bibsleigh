﻿using System;

namespace XFit.io
{
    internal class Fancy
    {
        private const string callTemplate = @"<!DOCTYPE html>
<html>
<head>
	<meta http-equiv=""Content-Type"" content=""text/html; charset=UTF-8""/>
	<meta name=""keywords"" content=""software linguistics, software language engineering, book of knowledge, glossary, academic publications, scientific research, open knowledge, open science""/>
	<title>BibSLEIGH — {0} call</title>
	<link href=""../stuff/bib.css"" rel=""stylesheet"" type=""text/css""/>
	<link href='http://fonts.googleapis.com/css?family=Exo+2:400,700,400italic,700italic' rel='stylesheet' type='text/css'>
	<script src=""../stuff/jquery.min.js"" type=""text/javascript""></script>
</head>
<body>
<div class=""left"">
	<a href=""../index.html""><img src=""../stuff/bibsleigh.png"" alt=""BibSLEIGH"" title=""BibSLEIGH"" class=""pad""/></a>

	<div class=""pad"">
		<a href=""../index.html""><img src=""../stuff/p-corpus.png"" alt=""BibSLEIGH corpus"" title=""All papers in the corpus""/></a><br/>
		<a href=""../tag/index.html""><img src=""../stuff/a-tags.png"" alt=""BibSLEIGH tags"" title=""All known tags""/></a><br/>
		<a href=""../bundle/index.html""><img src=""../stuff/p-bundles.png"" alt=""BibSLEIGH bundles"" title=""All selected bundles""/></a><br/>
		<a href=""../person/index.html""><img src=""../stuff/p-people.png"" alt=""BibSLEIGH people"" title=""All contributors""/></a><br/>
<a href=""https://github.com/slebok/bibsleigh/edit/master/calls/{0}.cfp""><img src=""../stuff/edit.png"" alt=""EDIT!"" title=""EDIT!""/></a>
	</div>
	<a href=""http://creativecommons.org/licenses/by/4.0/"" title=""CC-BY""><img src=""../stuff/cc-by.png"" alt=""CC-BY""/></a><br/>
	<a href=""http://opendatacommons.org/licenses/by/summary/"" title=""Open Knowledge""><img src=""../stuff/open-knowledge.png"" alt=""Open Knowledge"" /></a><br/>
	<a href=""http://validator.w3.org/check/referer"" title=""XHTML 1.0 W3C Rec""><img src=""../stuff/xhtml.png"" alt=""XHTML 1.0 W3C Rec"" /></a><br/>
	<a href=""http://jigsaw.w3.org/css-validator/check/referer"" title=""CSS 2.1 W3C CanRec""><img src=""../stuff/css.png"" alt=""CSS 2.1 W3C CanRec"" class=""pad"" /></a><br/>
	<div class=""sm"">
		<a href=""mailto:vadim@grammarware.net""><img src=""../stuff/email.png"" alt=""email"" title=""Complain!"" /></a>
		<a href=""https://twitter.com/intent/tweet?screen_name=grammarware""><img src=""../stuff/twitter.png"" alt=""twitter"" title=""Mention!"" /></a>
	</div>

</div>
<div class=""main"">
<h2><span class=""ttl"">Call</span> of {1}</h2>
{2}
</div>
<hr style=""clear:both""/>
<div class=""last"">
	<em>
		<a href=""http://bibtex.github.io"">Bibliography of Software Language Engineering in Generated Hypertext</a>
		(<a href=""http://github.com/slebok/bibsleigh"">BibSLEIGH</a>) is
		created and maintained by <a href=""http://grammarware.github.io/"">Dr. Vadim Zaytsev</a>.<br/>
		Hosted as a part of <a href=""http://slebok.github.io/"">SLEBOK</a> on <a href=""http://www.github.com/"">GitHub</a>.
	</em>
</div>
</body>
</html>";

        public static string FormatCall(string conference, string content)
        {
            string confname = conference;
            if (confname.Length > 6 && Char.IsDigit(confname[confname.Length - 1]) && Char.IsDigit(confname[confname.Length - 2]) && Char.IsDigit(confname[confname.Length - 3]) && Char.IsDigit(confname[confname.Length - 4]) && confname[confname.Length - 5] == '-')
                confname = confname.Substring(0, confname.LastIndexOf('-')) + " " + confname.Substring(confname.Length - 4);
            return String.Format(callTemplate, conference, confname, content);
        }

        public static string Times(string w, int t)
        {
            string result = String.Empty;
            for (int i = 0; i < t; i++)
                result += w;
            return result;
        }

        public static string DeUmlautify(string x)
            => x
                .Replace("ä", "ae")
                .Replace("ë", "e")
                .Replace("ü", "ue")
                .Replace("ö", "oe")
            ;
    }
}
