using System.Collections.Generic;
using XFit.io;

namespace XFit.ast
{
    internal class Domain
    {
        private string FileName;
        private readonly Sleigh Parent;

        internal string Name;
        internal readonly Dictionary<string, int> Tagged = new Dictionary<string, int>();
        internal string Title;
        internal string Venue;
        internal string EventUrl;
        internal readonly List<Brand> Brands = new List<Brand>();
        internal readonly List<Year> Years = new List<Year>();

        internal Domain(Sleigh parent)
        {
            Parent = parent;
        }

        internal void FromDisk(string path)
        {
            FileName = path;
            Parser.JSONtoDomain(path, this);
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
