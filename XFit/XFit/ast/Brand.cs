using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using XFit.refine;
using XFit.io;

namespace XFit.ast
{
    public class Brand : Serialisable
    {
        [JsonConverter(typeof(RelFlatStr3IntConverter))]
        public Dictionary<Tuple<string, string, string>, int> collocations = new Dictionary<Tuple<string, string, string>, int>();

        public string name;
        public string dblpurl;
        public string dblpkey;
        public string eventtitle;
        public string eventurl;

        [JsonConverter(typeof(ListFriendlyConverter))]
        public List<string> select;

        public string title;
        public string twitter;

        [JsonConverter(typeof(RelStrIntConverter))]
        public Dictionary<string, int> tagged = new Dictionary<string, int>();

        [JsonConverter(typeof(RelFlatStrIntConverter))]
        public Dictionary<string, int> vocabulary = new Dictionary<string, int>();

        public string venue; // TODO: ban?

        internal Brand()
        {
        }

        public override void Accept(CorpusVisitor v)
            => v.VisitBrand(this);
    }
}
