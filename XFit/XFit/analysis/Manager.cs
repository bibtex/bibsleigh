using System.Collections.Generic;
using XFit.ast;

namespace XFit.analysis
{
    internal static class Manager
    {
        private static IEnumerable<CorpusVisitor> checkers = new List<CorpusVisitor>()
        {
            new EmptyVenueFinder(),
        };

        internal static void FullAnalysis(Sleigh root)
        {
            foreach (var tool in checkers)
                root.Accept(tool);
        }
    }
}
