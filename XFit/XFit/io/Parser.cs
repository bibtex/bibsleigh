using Newtonsoft.Json;
using System;
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

        private static void CheckForUnusedKeys(string path, dynamic props)
        {
            foreach (var p in props)
            {
                var key = p.Name;
                if (!KnownKeys.Contains(key))
                    Logger.Log($"Unused key '{key}' in domain '{path}'!");
            }
        }

        internal static void JSONtoDomain(string path, Domain output)
            => JSONtoAST(path, output, ParseDomain);


        internal static void JSONtoBrand(string path, Brand output)
            => JSONtoAST(path, output, ParseBrand);

        private static void JSONtoAST<T>(string path, T output, Action<string, dynamic, T> parse)
        {
            dynamic brand = JsonConvert.DeserializeObject(File.ReadAllText(path));
            parse(path, brand, output);
            CheckForUnusedKeys(path, brand.Properties());
        }
    }
}
