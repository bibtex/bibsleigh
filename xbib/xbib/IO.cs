using System;
using System.Json;

namespace xbib
{
    internal static class IO
    {
        internal static XbCondition ParseCondition(string cond)
        {
            var words = cond.Split(' ');
            if (words.Length == 2 && words[0] == "when")
                return new XcExistsKey(words[1]);
            else if (words.Length == 3 && words[0] == "when" && words[1] == "no")
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
            else if (words.Length == 3 && words[0] == "rename" && words[1] == "to")
                return new XaRenameTo(context, words[2]);
            else if (words.Length == 3 && words[0] == "truncate" && words[1] == "left")
                return new XaTruncateLeft(context, Int32.Parse(words[2]));
            else if (words.Length == 3 && words[0] == "truncate" && words[1] == "right")
                return new XaTruncateRight(context, Int32.Parse(words[2]));
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

        internal static string BareValue(JsonValue json)
        {
            string value = json.ToString();
            if (value.Length > 2 && value[0] == '"' && value[value.Length - 1] == '"')
                value = value.Substring(1, value.Length - 2);
            return value;
        }
    }
}