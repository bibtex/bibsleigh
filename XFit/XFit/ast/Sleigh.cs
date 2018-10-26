using System.Collections.Generic;
using XFit.io;

namespace XFit.ast
{
    public class Sleigh : Serialisable
    {
        private readonly List<Domain> Domains = new List<Domain>();

        public int NoOfDomains
        {
            get => Domains.Count;
        }

        internal Sleigh()
        {
            Parent = null;
        }

        internal Sleigh(string path) : this()
        {
            FileName = path;
            foreach (var file in Walker.EveryJSON(path))
                AddDomain(file);
        }

        private void AddDomain(string file)
        {
            //if (!file.EndsWith("GRAPH.json", System.StringComparison.Ordinal))
            //    return;
            Domain domain = Parser.Parse<Domain>(file);
            domain.Parent = this;
            domain.FileName = file;
            domain.Descend();
            Logger.Log($"Domain '{domain.name}' added with {domain.NoOfPapers} papers.");
            Domains.Add(domain);
        }
    }
}
