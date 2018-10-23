using System;
using System.Collections.Generic;
using System.IO;

namespace XFit.io
{
    internal static class Walker
    {
        internal static IEnumerable<string> EveryJSON(string path)
            => Directory.GetFiles(path, "*.json", SearchOption.TopDirectoryOnly);
        internal static IEnumerable<string> EveryDir(string path)
        {
            var r = Directory.GetDirectories(path, "*", SearchOption.TopDirectoryOnly);
            Logger.Log($"EVERYTHING from '{path}' IS [{String.Join(",", r)}]");
            return r;
        }

        internal static bool FileExists(string path)
            => File.Exists(path);

        internal static bool DirExists(string path)
            => Directory.Exists(path);

        internal static bool Exists(string path)
            => FileExists(path) || DirExists(path);

        internal static string PureName(string path)
            => Path.GetFileNameWithoutExtension(path);

        internal static string DropExtension(string path)
        {
            string result = Path.ChangeExtension(path, "");
            if (result.EndsWith(".", System.StringComparison.Ordinal))
                result = result.Substring(0, result.Length - 1);
            return result;
        }
    }
}
