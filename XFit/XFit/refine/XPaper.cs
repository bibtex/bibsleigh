using System;
using XFit.ast;

namespace XFit.refine
{
    internal class XPaper : Xformation
    {
        private Func<Paper, Paper> _a;

        internal XPaper(Func<Paper, Paper> action)
        {
            _a = action;
        }

        public Serialisable Transform(Serialisable serialisable)
            => Transform(serialisable as Paper);

        internal Paper Transform(Paper input)
        {
            if (_a == null || input == null)
                return input;
            else
                return _a(input);
        }
    }
}
