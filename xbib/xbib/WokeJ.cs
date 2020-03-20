using System;
using System.IO;
using System.Json;
using System.Linq;
using System.Text;

namespace xbib
{
    internal class WokeJ
    {
        private static readonly string[] FormattedVertically =
        {
            "roles",
            "tagged",
        };

        internal static void ForAllElements(JsonArray json, Action<JsonValue> act)
        {
            for (int i = 0; i < json.Count; i++)
                act(json[i]);
        }

        internal static void ForAllElements(JsonArray json, Action<int, JsonValue> act)
        {
            for (int i = 0; i < json.Count; i++)
                act(i, json[i]);
        }

        internal static JsonValue GetElementByKey(JsonValue target, string key)
        {
            JsonObject json = target as JsonObject;
            if (json == null || !json.ContainsKey(key))
                return null;
            return json[key];
        }

        internal static void AddKeyValue(JsonValue target, string key, JsonValue value)
        {
            var old = GetElementByKey(target, key);
            if (old == null) // will be new
                target[key] = value;
            else
            {
                if (value is JsonObject) // NB: no fancy deep matching when (re)assigning an object
                    target[key] = value;
                else if (value is JsonArray neuA) // assigning from an array is the same as iterating over values
                {
                    ForAllElements(neuA, e => AddKeyValue(target, key, e));
                    return;
                }
                else // from now on we know neu is JsonPrimitive
                if (old is JsonPrimitive oldP)
                {
                    if (oldP == value)
                        return;
                    else
                        target[key] = value;
                }
                else if (old is JsonArray oldA)
                {
                    if (oldA.Contains(value)) // already on the list
                        return;
                    else
                        oldA.Add(value);
                }
                else // NB: no fancy deep matching when (re)assigning an object
                    target[key] = value;
            }
        }

        internal static JsonValue ParseJson(string filename)
        {
            try
            {
                return JsonValue.Parse(File.ReadAllText(filename));
            }
            catch (ArgumentException ae)
            {
                Console.WriteLine($"[ERROR] Cannot parse {filename}: {ae.Message}");
                return null;
            }
        }

        internal static string UnParseJson(JsonValue json)
        {
            StringBuilder sb = new StringBuilder();
            UnparseJson2("", json, sb);
            return sb.ToString();
        }

        private static void UnparseJson2(string key, JsonValue json, StringBuilder sb)
        {
            if (json is JsonArray ja)
            {
                if (FormattedVertically.Contains(key))
                    UnparseJson4(ja, sb);
                else
                    UnparseJson3(ja, sb);
            }
            else if (json is JsonObject jo)
                UnparseJson3(jo, sb);
            else if (json is JsonPrimitive jp)
                UnparseJson3(jp, sb);
        }

        private static void UnparseJson3(JsonPrimitive jp, StringBuilder sb)
        {
            sb.Append(jp.ToString());
        }

        private static void UnparseJson3(JsonObject jo, StringBuilder sb)
        {
            sb.Append("{" + Environment.NewLine);
            int i = 0, j = jo.Count - 1;
            foreach (string k in jo.Keys)
            {
                sb.Append("\t\"");
                sb.Append(k);
                sb.Append("\": ");
                UnparseJson2(k, jo[k], sb);
                if (i != j)
                    sb.Append(",");
                sb.Append(Environment.NewLine);
                i++;
            }
            sb.Append("}" + Environment.NewLine);
        }

        private static void UnparseJson3(JsonArray ja, StringBuilder sb)
        {
            sb.Append("[");
            ForAllElements(ja, (i, e) =>
                {
                    UnparseJson2("", e, sb);
                    if (i != ja.Count - 1)
                        sb.Append(", ");
                });
            sb.Append("]");
        }

        private static void UnparseJson4(JsonArray ja, StringBuilder sb)
        {
            sb.Append("[");
            ForAllElements(ja, (i, e) =>
            {
                UnparseJson2("", e, sb);
                if (i != ja.Count - 1)
                {
                    sb.Append(",");
                    sb.Append(Environment.NewLine);
                    sb.Append("\t\t");
                }
            });
            sb.Append("]");
        }
    }
}