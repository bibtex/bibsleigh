using System;
using XFit.ast;

namespace XFit.analysis
{
    internal class PaperAction : RefAction
    {
        private Func<Paper, Paper> _a;

        internal PaperAction(Func<Paper, Paper> action)
        {
            _a = action;
        }

        internal Paper Transform(Paper input)
        {
            if (_a == null)
                return input;
            else
                return _a(input);
        }
    }
}
