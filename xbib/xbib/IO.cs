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
            else if (words.Length == 4 && words[0] == "when" && words[2] == "==")
                return new XcMatchesExactly(words[1], words[3].Replace('_', ' '));
            else if (words.Length == 4 && words[0] == "when" && words[2] == "=^=")
                return new XcMatchesParentExactly(words[1], words[3]);
            else if (words.Length == 4 && words[0] == "when" && words[2] == "=~")
                return new XcMatchesLeft(words[1], words[3].Replace('_', ' '));
            else if (words.Length == 4 && words[0] == "when" && words[2] == "~=")
                return new XcMatchesRight(words[1], words[3].Replace('_', ' '));
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
            else if (words.Length == 2 && words[0] == "assign")
                return new XaAssign(context, words[1].Replace('_', ' '));
            else if (words.Length == 3 && words[0] == "add")
                return new XaAssign(words[1], words[2].Replace('_', ' '));
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
                XbCondition guard = null;
                string ctx;
                do
                {
                    var newguard = ParseCondition(line);
                    ctx = newguard.GetContext();
                    guard = CombineConditions(guard, newguard);
                    i++;
                    line = text[i].Trim();
                } while (IsCondition(line));
                var act = ParseAction(line, ctx);
                i++;
                return new XrGuardedAction(guard, act);
            }
            else
                throw new NotImplementedException("wrong xbib command: " + line);
        }

        private static XbCondition CombineConditions(XbCondition guard, XbCondition newguard)
            => guard == null ? newguard : new XcConjunction(guard, newguard);

        private static bool IsCondition(string line)
            => line.StartsWith("when ");

        internal static string BareValue(JsonValue json)
        {
            string value = json?.ToString();
            if (String.IsNullOrEmpty(value))
                return String.Empty;
            if (value.Length > 2 && value[0] == '"' && value[value.Length - 1] == '"')
                value = value.Substring(1, value.Length - 2);
            return value;
        }
    }
}