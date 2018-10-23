using Newtonsoft.Json;
using System.Collections.Generic;
using XFit.io;

namespace XFit.ast
{
    public class Domain
    {
        internal string FileName { get; set; }
        internal Sleigh Parent { get; set; }

        public string name;

        [JsonConverter(typeof(RelStrIntConverter))]
        public Dictionary<string, int> tagged = new Dictionary<string, int>();
        public string title;
        public string venue;
        public string eventurl;

        [JsonConverter(typeof(ListFriendlyConverter))]
        internal readonly List<Brand> Brands = new List<Brand>();

        [JsonConverter(typeof(ListFriendlyConverter))]
        internal readonly List<Year> Years = new List<Year>();

        internal Domain()
        {
        }

        internal void FromDisk(string path)
        {
            FileName = path;

            //if (Walker.FileExists(path))
            //{
            //    dynamic thing = JsonConvert.DeserializeObject(File.ReadAllText(path));
            //    parse(path, thing, output);
            //    CheckForUnusedKeys(path, thing.Properties(), where);
            //}
            //else
            //    parse(path, null, output);
        }

        internal void AddBrand(string file)
        {
            Brand brand = new Brand(this);
            brand.FromDisk(file);
            Brands.Add(brand);
        }

        internal void AddYear(string file)
        {
            Year year = new Year(this);
            year.FromDisk(file);
            Years.Add(year);
        }
    }
}
