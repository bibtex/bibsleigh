using System.Collections.Generic;
using XFit.io;

namespace XFit.ast
{
    internal class Domain
    {
        private readonly Sleigh Parent;

        internal string Name;
        internal readonly Dictionary<string, int> Tagged = new Dictionary<string, int>();
        internal string Title;
        internal string Venue;
        internal string EventUrl;
        internal readonly List<Brand> Brands = new List<Brand>();
        internal readonly List<Year> Years = new List<Year>();

        internal Domain(Sleigh parent, string path)
        {
            Parent = parent;
            Parser.JSONtoDomain(path, this);
        }
    }
}
