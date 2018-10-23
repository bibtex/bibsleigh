using System.Collections.Generic;
using XFit.io;

namespace XFit.ast
{
    internal class Brand : Serialisable
    {
        private string FileName;
        private readonly Domain Parent;

        internal string Name;
        internal string Title;
        internal string Twitter;
        internal readonly Dictionary<string, int> Tagged = new Dictionary<string, int>();
        internal readonly List<string> Selected = new List<string>();
        internal readonly Dictionary<string, int> Vocabulary = new Dictionary<string, int>();
        internal string DblpUrl;
        internal string DblpKey;

        internal Brand(Domain parent)
        {
            Parent = parent;
        }

        public void FromDisk(string path)
        {
            FileName = path;
            Parser.JSONtoBrand(path, this);
        }
    }
}
