using XFit.io;

namespace XFit.ast
{
    internal class Brand : Serialisable
    {
        private string FileName;
        private readonly Domain Parent;

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
