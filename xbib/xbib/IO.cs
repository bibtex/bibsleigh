using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;

namespace xbib
{
    internal static class IO
    {
        private static JsonSerializerSettings _settings = new JsonSerializerSettings
        {
            DefaultValueHandling = DefaultValueHandling.Ignore,
            MissingMemberHandling = MissingMemberHandling.Error,
            NullValueHandling = NullValueHandling.Ignore
        };

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
                    Console.WriteLine($"Unused key '{key}' in {where} '{path}'!");
            }
        }

        public static T Parse<T>(string fname)
            => ParseText<T>(File.ReadAllText(fname));

        public static T ParseText<T>(string text)
            => JsonConvert.DeserializeObject<T>(text, _settings);

        public static string Unparse(object thing)
        {
            string result = JsonConvert.SerializeObject(thing, Formatting.Indented, _settings).Replace("  ", "\t");
            // The following is not strictly needed, but used for comparison
            //result = result.Replace("\r\n\t\t", " ").Replace(": [ ", ": [").Replace("\r\n\t],", "],");
            return result;
        }

        public static void Unparse(object thing, string fname)
            => File.WriteAllText(fname, Unparse(thing));

        public static T Clone<T>(T c)
            => ParseText<T>(Unparse(c));
    }
}