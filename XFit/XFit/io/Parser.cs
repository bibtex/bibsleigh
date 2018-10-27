using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.IO;

namespace XFit.io
{
    public static partial class Parser
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
                    Logger.Log($"Unused key '{key}' in {where} '{path}'!");
            }
        }

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

        public static T Parse<T>(string fname)
        {
            string contents = File.ReadAllText(fname);
            T thing = JsonConvert.DeserializeObject<T>(contents, _settings);
            return thing;
        }

        public static string Unparse(object thing)
        {
            string result = JsonConvert.SerializeObject(thing, Formatting.Indented, _settings).Replace("  ", "\t");
            // The following is not strictly needed, but used for comparison
            //result = result.Replace("\r\n\t\t", " ").Replace(": [ ", ": [").Replace("\r\n\t],", "],");
            return result;
        }

        public static void Unparse(object thing, string fname)
            => File.WriteAllText(fname, Unparse(thing));
    }
}
