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
                Console.WriteLine("[ERROR] Cannot parse " + filename);
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

        internal static XBibCondition ParseCondition(string cond)
        {
            if (cond.StartsWith("when no "))
                return new XBibNegation(new XBibExistsKey(cond.Substring(8).Trim()));
            else
                throw new NotImplementedException($"condition '{cond}' not recognised");
        }

        internal static XBibAction ParseAction(string act, string context)
        {
            if (act == "take from parent")
                return new XBibTakeFromParent(context);
            else
                throw new NotImplementedException($"action '{act}' not recognised");
        }
    }
}