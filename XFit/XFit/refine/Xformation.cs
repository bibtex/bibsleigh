using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using XFit.ast;

namespace XFit.refine
{
    internal interface Xformation
    {
        Serialisable Transform(Serialisable serialisable);
    }
}
