using System.Collections.Generic;
using XFit.io;

namespace XFit.ast
{
    internal class Year : Serialisable
    {
        private string FileName;
        private readonly Domain Parent;

        private List<Conference> Confs = new List<Conference>();

        internal Year(Domain parent)
        {
            Parent = parent;
        }

        public void FromDisk(string path)
        {
            FileName = path;
            Parser.JSONtoYear(path, this);
        }

        internal void AddConf(string path)
        {
            Conference conf = new Conference(this);
            conf.FromDisk(path);
            Confs.Add(conf);
        }
    }
}
