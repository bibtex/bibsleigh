using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using XFit.io;

namespace XFit.ast
{
    public class Brand : Serialisable
    {
        private string FileName;
        private readonly Domain Parent;

        [JsonConverter(typeof(RelFlatStr3IntConverter))]
        public Dictionary<Tuple<string, string, string>, int> collocations = new Dictionary<Tuple<string, string, string>, int>();

        public string name;

        [JsonConverter(typeof(ListFriendlyConverter))]
        public List<string> select;

        public string title;
        public string twitter;

        [JsonConverter(typeof(RelStrIntConverter))]
        public Dictionary<string, int> tagged = new Dictionary<string, int>();

        [JsonConverter(typeof(RelFlatStrIntConverter))]
        public Dictionary<string, int> vocabulary = new Dictionary<string, int>();
        public string dblpurl;
        public string dblpkey;

        internal Brand()
        {
        }

        internal Brand(Domain parent) : this()
        {
            Parent = parent;
        }

        public void FromDisk(string path)
        {
            FileName = path;
            Parser.JSONtoBrand(path, this);
        }
    }
}
