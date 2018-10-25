using System.Collections.Generic;
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
            // TODO: descend!
            Confs.Add(conf);
        }
    }
}
