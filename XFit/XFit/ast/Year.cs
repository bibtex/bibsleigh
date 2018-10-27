using System.Collections.Generic;
using System.Linq;
using XFit.analysis;
using XFit.io;

namespace XFit.ast
{
    public class Year : Serialisable
    {
        private List<Conference> Confs = new List<Conference>();

        internal Year(Domain parent, string path)
        {
            Parent = parent;
            FileName = path;
            foreach (var file in Walker.EveryJSON(path))
                AddConf(file);
        }

        internal void AddConf(string path)
        {
            Conference conf = Parser.Parse<Conference>(path);
            conf.Parent = this;
            conf.FileName = path;
            conf.Descend();
            Confs.Add(conf);
        }

        public int NoOfPapers
        {
            get => Confs.Sum(c => c.NoOfPapers);
        }

        public override void Accept(CorpusVisitor v)
        {
            v.VisitYear(this);
            foreach (var conf in Confs)
                conf.Accept(v);
        }
    }
}
