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
                "collocations", // not fully
                "dblpkey",
                "dblpurl",
                "eventurl",
                "name",
                "select",
                "tagged",
                "title",
                "twitter",
                "venue",
                "vocabulary",
            };

        internal static void ParseListStr(dynamic json, List<string> output)
        {
            output.Clear();
            if (json != null)
                foreach (dynamic elem in json)
                    output.Add((string)elem);
        }

        internal static void ParseDictStrInt(dynamic json, Dictionary<string, int> output)
        {
            output.Clear();
            if (json != null)
                foreach (dynamic elem in json)
                    output[(string)elem[0]] = (int)elem[1];
        }

        internal static void ParseFlatDictStrInt(dynamic json, Dictionary<string, int> output)
        {
            output.Clear();
            bool word = true;
            string name = "";
            if (json != null)
                foreach (dynamic elem in json)
                {
                    if (word)
                        name = (string)elem;
                    else
                        output[name] = (int)elem;
                    word = !word;
                }
        }

        private static void CheckForUnusedKeys(string path, dynamic props, string where)
        {
            foreach (var p in props)
            {
                var key = p.Name;
                if (!KnownKeys.Contains(key))
                    Logger.Log($"Unused key '{key}' in {where} '{path}'!");
            }
        }

        internal static void JSONtoDomain(string path, Domain output)
            => JSONtoAST(path, output, ParseDomain, "domain");

        internal static void JSONtoBrand(string path, Brand output)
            => JSONtoAST(path, output, ParseBrand, "brand");

        internal static void JSONtoYear(string path, Year output)
           => JSONtoAST(path, output, ParseYear, "year");

        internal static void JSONtoConf(string path, Conference output)
            => JSONtoAST(path, output, ParseConf, "conference");

        private static void JSONtoAST<T>(string path, T output, Action<string, dynamic, T> parse, string where)
        {
            if (Walker.FileExists(path))
            {
                dynamic thing = JsonConvert.DeserializeObject(File.ReadAllText(path));
                parse(path, thing, output);
                CheckForUnusedKeys(path, thing.Properties(), where);
            }
            else
                parse(path, null, output);
        }
    }
}
