using System.Collections.Generic;
using XFit.io;

namespace XFit.ast
{
    internal class Sleigh : Serialisable
    {
        private string FileName;
        private readonly List<Domain> Domains = new List<Domain>();

        public int NoOfDomains
        {
            get => Domains.Count;
        }

        internal Sleigh()
        {
        }

        internal Sleigh(string path) : this()
        {
            FromDisk(path);
        }

        public void FromDisk(string path)
        {
            FileName = path;
            foreach (var file in Walker.EveryJSON(path))
                AddDomain(file);
        }

        private void AddDomain(string file)
        {
            Domain domain = new Domain(this);
            domain.FromDisk(file);
            Domains.Add(domain);
        }
    }
}
