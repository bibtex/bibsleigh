using System.Collections.Generic;
using System.IO;
using XFit.ast;

namespace XFit.io
{
    internal static class Walker
    {
        internal static IEnumerable<string> EveryJSON(string path)
            => DirExists(path)
            ? Directory.GetFiles(path, "*.json", SearchOption.TopDirectoryOnly)
            : new string[0];

        internal static IEnumerable<string> EveryDir(string path)
        {
            if (!DirExists(path))
                return new string[0];
            var r = Directory.GetDirectories(path, "*", SearchOption.TopDirectoryOnly);
            //Logger.Log($"EVERYTHING from '{path}' IS [{String.Join(",", r)}]");
            return r;
        }

        internal static IEnumerable<string> EveryCfP(string path)
            => DirExists(path)
            ? Directory.GetFiles(path, "*.cfp", SearchOption.TopDirectoryOnly)
            : new string[0];

        internal static bool FileExists(string path)
            => File.Exists(path);

        internal static bool DirExists(string path)
            => Directory.Exists(path);

        internal static bool Exists(string path)
            => FileExists(path) || DirExists(path);

        internal static string PureName(Serialisable thing)
            => Path.GetFileNameWithoutExtension(thing.FileName);

        internal static string PureName(string path)
            => Path.GetFileNameWithoutExtension(path);

        internal static string DropExtension(string path)
        {
            string result = Path.ChangeExtension(path, "");
            if (result.EndsWith(".", System.StringComparison.Ordinal))
                result = result.Substring(0, result.Length - 1);
            return result;
        }

        internal static string PathToCfPs(string path)
        {
            path = TrimPath(path);
            if (path.EndsWith("corpus", System.StringComparison.Ordinal))
                path = path.Substring(0, path.Length - 6);
            else
                path = Path.Combine(path, "..");
            return Path.Combine(path, "calls");
        }

        internal static string PathToHTMLs(string path)
        {
            path = TrimPath(path);
            if (path.EndsWith("corpus", System.StringComparison.Ordinal))
                path = path.Substring(0, path.Length - 6);
            else
                path = Path.Combine(path, "..");
            path = TrimPath(path);
            if (path.EndsWith("json", System.StringComparison.Ordinal))
                path = path.Substring(0, path.Length - 4);
            else
                path = Path.Combine(path, "..");
            return Path.Combine(path, "frontend");
        }

        internal static string TrimPath(string path)
            => path[path.Length - 1] == '/' || path[path.Length - 1] == '\\'
            ? path.Substring(0, path.Length - 1)
            : path;
    }
}
