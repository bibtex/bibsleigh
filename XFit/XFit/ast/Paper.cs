using Newtonsoft.Json;
using System.Collections.Generic;
using System.IO;
using XFit.io;

namespace XFit.ast
{
    public class Paper
    {
        private string FileName;
        private Conference Parent;

        [JsonConverter(typeof(ListFriendlyConverter))]
        public List<string> author = new List<string>();

        public string booktitle;
        public string crossref;
        public string dblpkey;
        public string dblpurl;
        public string doi;
        public string pages;
        public string publisher;
        public List<string> stemmed = new List<string>();
        public List<string> tag = new List<string>();
        public string title;
        public string type;
        public string venue;
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
