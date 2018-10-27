using Newtonsoft.Json;
using System.Collections.Generic;
using System.IO;
using XFit.analysis;
using XFit.io;

namespace XFit.ast
{
    public class Paper : Serialisable
    {
        public string acmid; // can be 99999999.999999
        public List<string> address; // Should be a tuple?

        [JsonConverter(typeof(ListFriendlyConverter))]
        public List<string> author;

        public string booktitle;
        public string booktitleshort;

        // do we care about a path to the PDF on some long gone CD?
        [JsonConverter(typeof(ListFriendlyConverter))]
        public List<string> cdrom;

        // TODO: verify and use more extensively? or reserve for Zeitgeist?
        [JsonConverter(typeof(ListFriendlyConverter))]
        public List<string> cite;

        public string crossref;
        public string dblpkey;
        public string dblpurl;
        public string doi;

        [JsonConverter(typeof(ListFriendlyConverter))]
        public List<string> editor;

        [JsonConverter(typeof(ListFriendlyConverter))]
        public List<string> ee; // refactoring opportunities

        public int ieeearid;
        public int ieeeisid;
        public int ieeepuid;
        public string ieeeurl; // http://www.computer.org/...

        [JsonConverter(typeof(ListFriendlyConverter))]
        public List<string> isbn; // at some point move to one?

        public int issue;
        public string journal;
        public string journalshort;
        public string month;
        public string note; // semantics unclear, possible refactoring target
        public string number;
        public string openpdf; // merge with pdfurl?
        public string pages;
        public string pagesroman; // normalise and sort well
        public string pdfurl; // merge with openpdf?
        public string publisher;
        public string publishershort;
        public string series;
        public string seriesshort; // LNCS

        // "keynote", "tool demo", "invited", "influential", etc (ref opp!)
        [JsonConverter(typeof(ListFriendlyConverter))]
        public List<string> status;

        public List<string> stemmed;
        public List<string> tag;
        public string title;
        public string type;
        public string url; // semantics unclear, possible refactoring target
        public string venue;
        public string volume;
        public int year;

        public Paper()
        {
        }

        public Paper(Conference conference, string file)
        {
            FileName = file;
            Parent = conference;
            dynamic domain = JsonConvert.DeserializeObject(File.ReadAllText(file));
        }

        public override void Accept(CorpusVisitor v)
            => v.VisitPaper(this);
    }
}
