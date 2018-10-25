using Newtonsoft.Json;
using System.Collections.Generic;
using System.IO;
using XFit.io;

namespace XFit.ast
{
    public class Paper : Serialisable
    {
        public string acmid; // can be 99999999.999999
        public int ieeearid;
        public int ieeeisid;
        public int ieeepuid;
        public string ieeeurl; // http://www.computer.org/...

        // do we care about a path to the PDF on some long gone CD?
        [JsonConverter(typeof(ListFriendlyConverter))]
        public List<string> cdrom = new List<string>();

        public List<string> address = new List<string>(); // Should be a tuple?

        [JsonConverter(typeof(ListFriendlyConverter))]
        public List<string> author = new List<string>();

        public string booktitle;
        public string booktitleshort;

        // TODO: verify and use more extensively? or reserve for Zeitgeist?
        [JsonConverter(typeof(ListFriendlyConverter))]
        public List<string> cite = new List<string>();

        public string crossref;
        public string dblpkey;
        public string dblpurl;
        public string doi;

        [JsonConverter(typeof(ListFriendlyConverter))]
        public List<string> editor = new List<string>();

        [JsonConverter(typeof(ListFriendlyConverter))]
        public List<string> ee = new List<string>(); // refactoring opportunities

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
        public List<string> status = new List<string>();

        public List<string> stemmed = new List<string>();
        public List<string> tag = new List<string>();
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
    }
}
