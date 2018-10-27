using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using XFit.analysis;
using XFit.io;

namespace XFit.ast
{
    public class Conference : Serialisable
    {
        private string DirName;

        public string acmid; // can be 99999999.999999
        public int ieeeisid;
        public int ieeepuid;
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

        internal void Descend()
        {
            if (String.IsNullOrEmpty(FileName))
            {
                Logger.Log($"Unknown location of conference '{title}', skipped");
                return;
            }
            DirName = Walker.DropExtension(FileName);
            if (!Walker.DirExists(DirName))
            {
                Logger.Log($"No papers in conference {Walker.PureName(DirName)} ('{title}'), skipped");
                return;
            }
            foreach (var file in Walker.EveryJSON(DirName))
                AddPaper(file);
        }

        internal void AddPaper(string file)
        {
            var paper = Parser.Parse<Paper>(file);
            paper.FileName = file;
            paper.Parent = this;
            Papers.Add(paper);
        }

        public int NoOfPapers
        {
            get => Papers.Count;
        }

        public override void Accept(CorpusVisitor v)
        {
            v.VisitConference(this);
            foreach (var paper in Papers)
                paper.Accept(v);
        }
    }
}
