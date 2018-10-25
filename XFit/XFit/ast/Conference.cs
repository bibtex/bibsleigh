using Newtonsoft.Json;
using System.Collections.Generic;
using System.IO;
using XFit.io;

namespace XFit.ast
{
    public class Conference : Serialisable
    {
        private string DirName;

        public int acmid;
        public int ieeepuid;
        public int ieeeisid;
        public string ieeeurl; // http://www.computer.org/...

        public List<string> address;
        public string booktitle;
        public string booktitleshort; // not used enough!
        public string key; // non-dblp for crossref
        public string dblpkey;
        public string dblpurl;
        public string doi;

        [JsonConverter(typeof(ListFriendlyConverter))]
        public List<string> editor = new List<string>();

        [JsonConverter(typeof(ListFriendlyConverter))]
        public List<string> ee = new List<string>();

        public string eventtitle;
        public string eventurl;

        [JsonConverter(typeof(ListFriendlyConverter))]
        public List<string> isbn = new List<string>();

        public int issue;

        public string journal;
        public string journalshort;

        public string number;
        public string organization;

        public string publisher;
        public string publishershort;

        public List<List<string>> roles = new List<List<string>>();

        public string series;
        public string seriesshort;

        [JsonConverter(typeof(RelStrIntConverter))]
        public Dictionary<string, int> tagged = new Dictionary<string, int>();

        public string title;
        public string twitter;
        public string type;
        public string venue;
        public string volume; // Usually an integer, but not always
        public string month; // used too rarely
        public string urn; // mostly a Dagstuhl thing
        public int year;

        public string pdfurl; // Proceedings!

        [JsonConverter(typeof(ListFriendlyConverter))]
        public List<string> programchair; // migrate to roles?
        [JsonConverter(typeof(ListFriendlyConverter))]
        public List<string> generalchair; // migrate to roles?

        private List<Paper> Papers = new List<Paper>();

        public Conference()
        {
        }

        public Conference(Year year, string path)
        {
            FileName = Path.ChangeExtension(path, "json");
            DirName = path;
            //Parser.JSONtoConf(path, this);
        }

        internal void AddPaper(string file)
        {
            Papers.Add(new Paper(this, file));
        }
    }
}
