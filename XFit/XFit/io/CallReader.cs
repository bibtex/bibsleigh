using System.IO;
using XFit.ast;

namespace XFit.io
{
    internal class CallReader
    {
        internal static Call Parse(string filename)
            => new Call(filename);

        internal static void UnParse(string filename, Call call)
            => File.WriteAllText(filename, Fancy.FormatCall(Walker.PureName(filename), call.ToString()));
    }
}
