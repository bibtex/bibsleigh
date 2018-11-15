using System.IO;
using XFit.ast;
using XFit.io.ht;

namespace XFit.io
{
    internal class CallReader
    {
        internal static Call Parse(string filename)
            => new Call(filename);

        internal static void UnParse(string path, string filename, Call call)
            => File.WriteAllText(Path.Combine(path, "call", filename), new HtCall(path, call).ToString());
    }
}
