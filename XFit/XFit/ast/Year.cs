using System.Collections.Generic;
using System.IO;

namespace XFit.ast
{
    internal class Year
    {
        private readonly Domain Parent;

        private List<Conference> Confs = new List<Conference>();

        internal Year(Domain parent, string path)
        {
            Parent = parent;
            Dictionary<string, string>
                jsons = new Dictionary<string, string>(),
                dirs = new Dictionary<string, string>();
            foreach (var file in Directory.GetFiles(path, "*", SearchOption.TopDirectoryOnly))
            {
                if (File.Exists(file))
                    jsons[Path.GetFileNameWithoutExtension(file)] = file;
                if (Directory.Exists(file))
                    dirs[Path.GetFileNameWithoutExtension(file)] = file;
            }
            foreach(var key in jsons.Keys)
            {
                if (!dirs.ContainsKey(key))
                    Logger.Log($"JSON without a directory: {key}");
                else
                    Confs.Add(new Conference(this, jsons[key], dirs[key]));
            }
        }
    }
}
