using XFit.refine;

namespace XFit.ast
{
    public abstract class Serialisable
    {
        internal Serialisable Parent;
        internal string FileName;

        public abstract void Accept(CorpusVisitor v);
    }
}
