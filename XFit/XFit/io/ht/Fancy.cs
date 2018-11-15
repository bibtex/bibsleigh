using System;

namespace XFit.io.ht
{
    internal class Fancy
    {
        protected const string BackOne = "../";
        protected const string Stuff = "stuff/";
        protected const string IndexHtml = "index.html";

        protected string RelativePath = "";
        protected string Title = "";
        protected bool IncludeJQuery = true;
        protected MenuItem ActiveMenuItem = MenuItem.None;
        protected string LeftTopIcon = "";
        protected string LeftTopLink = "";
        protected string EditPath = "";
        protected string Content = "";

        ////////////////////////////////////////////////////////////////////////////////

        private string HtHeader()
        {
            string template = @"<head>
	<meta http-equiv=""Content-Type"" content=""text/html; charset=UTF-8""/>
	<meta name=""keywords"" content=""software linguistics, software language engineering, book of knowledge, glossary, academic publications, scientific research, open knowledge, open science, bibliography, bibtex, survey, related work""/>
	<title>BibSLEIGH{2}</title>
	<link href=""{0}{1}bib.css"" rel=""stylesheet"" type=""text/css""/>
	<link href='http://fonts.googleapis.com/css?family=Exo+2:400,700,400italic,700italic' rel='stylesheet' type='text/css'>";
            if (IncludeJQuery)
                template += @"<script src=""{0}{1}jquery.min.js"" type=""text/javascript""></script>";
            template += "</head>" + Environment.NewLine;
            return String.Format(template,
                RelativePath,
                Stuff,
                String.IsNullOrEmpty(Title) ? "" : " — " + Title
                );
        }

        private string HtMenuItem(MenuItem item)
        {
            string path = RelativePath + Stuff + (item == ActiveMenuItem ? "a" : "p");
            switch (item)
            {
                case MenuItem.Corpus:
                    return $"<a href=\"{RelativePath}index.html\"><img src=\"{path}-corpus.png\" alt=\"BibSLEIGH corpus\" title=\"All papers in the corpus\"/></a><br/>";
                case MenuItem.Tags:
                    return $"<a href=\"{RelativePath}tag/index.html\"><img src=\"{path}-tags.png\" alt=\"BibSLEIGH tags\" title=\"All known tags\"/></a><br/>";
                case MenuItem.Bundles:
                    return $"<a href=\"{RelativePath}bundle/index.html\"><img src=\"{path}-bundles.png\" alt=\"BibSLEIGH bundles\" title=\"All selected bundles\"/></a><br/>";
                case MenuItem.Calls:
                    return $"<a href=\"{RelativePath}call/index.html\"><img src=\"{path}-calls.png\" alt=\"BibSLEIGH calls\" title=\"All collected calls for papers and participation\"/></a><br/>";
                case MenuItem.People:
                    return $"<a href=\"{RelativePath}person/index.html\"><img src=\"{path}-people.png\" alt=\"BibSLEIGH people\" title=\"All contributors\"/></a><br/>";
                default:
                    return "UNKNOWN ITEM";
            }
        }

        private string HtLeft()
        {
            var toplink = String.IsNullOrEmpty(LeftTopLink) ? (RelativePath + IndexHtml) : LeftTopLink;
            var topimg = RelativePath + Stuff + (String.IsNullOrEmpty(LeftTopIcon) ? "bibsleigh" : LeftTopIcon);

            string template = @"<div class=""left"">
	<a href=""{0}""><img src=""{1}.png"" alt=""{2}"" title=""{2}"" class=""pad""/></a>

	<div class=""pad"">
		{3}
		{4}
		{5}
		{6}
		{7}
{8}	</div>
	<a href=""http://creativecommons.org/licenses/by/4.0/"" title=""CC-BY""><img src=""{9}cc-by.png"" alt=""CC-BY""/></a><br/>
	<a href=""http://opendatacommons.org/licenses/by/summary/"" title=""Open Knowledge""><img src=""{9}open-knowledge.png"" alt=""Open Knowledge"" /></a><br/>
	<a href=""http://validator.w3.org/check/referer"" title=""XHTML 1.0 W3C Rec""><img src=""{9}xhtml.png"" alt=""XHTML 1.0 W3C Rec"" /></a><br/>
	<a href=""http://jigsaw.w3.org/css-validator/check/referer"" title=""CSS 2.1 W3C CanRec""><img src=""{9}css.png"" alt=""CSS 2.1 W3C CanRec"" class=""pad"" /></a><br/>
	<div class=""sm"">
		<a href=""mailto:vadim@grammarware.net""><img src=""{9}email.png"" alt=""email"" title=""Complain!"" /></a>
		<a href=""https://twitter.com/intent/tweet?screen_name=grammarware""><img src=""{9}twitter.png"" alt=""twitter"" title=""Mention!"" /></a>
	</div>
</div>";
            return String.Format(template,
                RelativePath + toplink,
                topimg,
                Title,
                HtMenuItem(MenuItem.Corpus),
                HtMenuItem(MenuItem.Tags),
                HtMenuItem(MenuItem.Bundles),
                HtMenuItem(MenuItem.Calls),
                HtMenuItem(MenuItem.People),
                String.IsNullOrEmpty(EditPath) ? "" : $"<a href=\"https://github.com/slebok/bibsleigh/edit/master/{EditPath}\"><img src=\"{RelativePath}{Stuff}edit.png\" alt=\"EDIT!\" title=\"EDIT!\"/></a>",
                RelativePath + Stuff
            );
        }

        private string HtFooter()
            => @"<hr style=""clear:both""/>
<div class=""last"">
	<em>
		<a href=""http://bibtex.github.io"">Bibliography of Software Language Engineering in Generated Hypertext</a>
		(<a href=""http://github.com/slebok/bibsleigh"">BibSLEIGH</a>) is
		created and maintained by <a href=""http://grammarware.github.io/"">Dr. Vadim Zaytsev</a>.<br/>
		Hosted as a part of <a href=""http://slebok.github.io/"">SLEBOK</a> on <a href=""http://www.github.com/"">GitHub</a>.
	</em>
</div>";

        public override string ToString()
        {
            string template = @"<!DOCTYPE html>
<html>
{0}
<body>
{1}
<div class=""main"">
{2}
</div>
{3}
</body>
</html>";
            return String.Format(template,
                HtHeader(),
                HtLeft(),
                Content,
                HtFooter()
                );
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
