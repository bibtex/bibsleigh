using Newtonsoft.Json;
using System.Collections.Generic;
using System.Linq;
using XFit.refine;
using XFit.io;

namespace XFit.ast
{
    public class Domain : Serialisable
    {
        public string name;

        [JsonConverter(typeof(RelStrIntConverter))]
        public Dictionary<string, int> tagged = new Dictionary<string, int>();
        public string title;
        public string venue;
        public string eventurl;

        internal readonly List<Brand> Brands = new List<Brand>();

        internal readonly List<Year> Years = new List<Year>();

        public int NoOfPapers
        {
            get => Years.Sum(y => y.NoOfPapers);
        }

        internal Domain()
        {
        }

        internal void Descend()
        {
            var dirname = Walker.DropExtension(FileName);
            foreach (var file in Walker.EveryJSON(dirname))
                AddBrand(file);
            foreach (var file in Walker.EveryDir(dirname))
                AddYear(file);
        }

        internal void AddBrand(string file)
        {
            Brand brand = Parser.Parse<Brand>(file);
            brand.Parent = this;
            brand.FileName = file;
            Brands.Add(brand);
        }

        internal void AddYear(string file)
        {
            Year year = new Year(this, file);
            Years.Add(year);
        }

        public override void Accept(CorpusVisitor v)
        {
            if (v.EnterDomain(this))
            {
                foreach (var brand in Brands)
                    brand.Accept(v);
                foreach (var year in Years)
                    year.Accept(v);
            }
            v.ExitDomain(this);
        }
    }
}
