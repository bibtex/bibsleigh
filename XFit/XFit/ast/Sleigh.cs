using System.Collections.Generic;
using XFit.io;

namespace XFit.ast
{
    internal class Sleigh
    {
        private readonly List<Domain> Domains = new List<Domain>();

        public int NoOfDomains
        {
            get => Domains.Count;
        }

        internal Sleigh(string path)
        {
            foreach (var file in Walker.EveryJSON(path))
                Domains.Add(new Domain(this, file));
        }
    }
}
