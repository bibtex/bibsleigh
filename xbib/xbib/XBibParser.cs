using System;
using System.IO;
using System.Json;
using System.Text;

namespace xbib
{
    internal static class XBibParser
    {
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
            UnparseJson2(json, sb);
            return sb.ToString();
        }

        private static void UnparseJson2(JsonValue json, StringBuilder sb)
        {
            if (json is JsonArray ja)
                UnparseJson3(ja, sb);
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
                UnparseJson2(jo[k], sb);
                // COMMA!
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
            for (int i = 0; i < ja.Count; i++)
            {
                UnparseJson2(ja[i], sb);
                if (i != ja.Count - 1)
                    sb.Append(", ");
            }
            sb.Append("]");
        }

        internal static XbCondition ParseCondition(string cond)
        {
            var words = cond.Split(' ');
            if (words.Length == 3 && words[0] == "when" && words[1] == "no")
                return new XcNegation(new XcExistsKey(words[2]));
            else if (words.Length == 4 && words[0] == "when" && words[2] == "=~")
                return new XcMatchesLeft(words[1], words[3]);
            else if (words.Length == 4 && words[0] == "when" && words[2] == "~=")
                return new XcMatchesRight(words[1], words[3]);
            else
                throw new NotImplementedException($"condition '{cond}' not recognised");
        }

        internal static XbAction ParseAction(string act, string context)
        {
            var words = act.Split(' ');
            if (words.Length == 2 && words[0] == "inherit")
                return new XaInherit(context, words[1]);
            else if (words.Length == 2 && words[0] == "remove")
                return new XaRemove(words[1]);
            else
                throw new NotImplementedException($"action '{act}' not recognised");
        }

        internal static XbRule ParseRule(string line, string[] text, ref int i)
        {
            if (i + 1 < text.Length)
            {
                string s1, s2;
                s1 = line;
                s2 = text[i + 1].Trim();
                i += 2;
                var guard = ParseCondition(s1);
                var act = ParseAction(s2, guard.GetContext());
                return new XrGuardedAction(guard, act);
            }
            else
                throw new NotImplementedException("wrong xbib command: " + line);
        }

        internal static string BareValue(JsonPrimitive json)
        {
            string value = json.ToString();
            if (value.Length > 2 && value[0] == '"' && value[value.Length - 1] == '"')
                value = value.Substring(1, value.Length - 2);
            return value;
        }
    }
}