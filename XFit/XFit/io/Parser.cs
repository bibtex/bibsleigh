using Newtonsoft.Json;
using System.Collections.Generic;
using System.IO;
using XFit.ast;

namespace XFit.io
{
    internal static partial class Parser
    {
        private static List<string> KnownKeys
            = new List<string> {
                "name",
                "title",
                "venue",
                "tagged",
                "eventurl",
            };

        internal static void ParseDictStrInt(dynamic json, Dictionary<string, int> output)
        {
            output.Clear();
            if (json != null)
                foreach (dynamic elem in json)
                    output[(string)elem[0]] = (int)elem[1];
        }

        internal static void JSONtoDomain(string path, Domain output)
        {
            dynamic domain = JsonConvert.DeserializeObject(File.ReadAllText(path));
            ParseDomain(path, domain, output);
            CheckForUnusedKeys(path, domain.Properties());
        }

        private static void CheckForUnusedKeys(string path, dynamic props)
        {
            foreach (var p in props)
            {
                var key = p.Name;
                if (!KnownKeys.Contains(key))
                    Logger.Log($"Unused key '{key}' in domain '{path}'!");
            }
        }
    }
}
