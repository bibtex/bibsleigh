using System;
using XFit.ast;

namespace XFit.analysis
{
    internal class XConf : Xformation
    {
        private Func<Conference, Conference> _a;

        internal XConf(Func<Conference, Conference> action)
        {
            _a = action;
        }

        public Serialisable Transform(Serialisable serialisable)
            => Transform(serialisable as Conference);

        internal Conference Transform(Conference input)
        {
            if (_a == null)
                return input;
            else
                return _a(input);
        }
    }
}
