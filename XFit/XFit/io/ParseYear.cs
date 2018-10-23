using System.Collections.Generic;
using XFit.ast;

namespace XFit.io
{
    internal static partial class Parser
    {
        private static void ParseYear(string path, dynamic input, Year output)
        {
            Dictionary<string, string>
                jsons = new Dictionary<string, string>(),
                dirs = new Dictionary<string, string>();
            foreach (var file in Walker.EveryJSON(path))
                jsons[Walker.PureName(file)] = file;
            foreach (var file in Walker.EveryDir(path))
                dirs[Walker.PureName(file)] = file;
            foreach (var key in jsons.Keys)
            {
                if (!dirs.ContainsKey(key))
                    Logger.Log($"JSON without a directory: {key}");
                else
                    output.AddConf(dirs[key]);
            }
        }
    }
}
