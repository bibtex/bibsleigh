using System;
using System.Collections.Generic;
using System.IO;
using XFit.io;

namespace XFit.ast
{
    public class Call
    {
        private string Content = String.Empty;

        public Call(string filename)
        {
            var lines = File.ReadAllLines(filename);
            foreach (var rawline in lines)
            {
                var line = rawline.Trim();
                var addline = rawline;
                if (String.IsNullOrEmpty(line))
                {
                    Content += rawline;
                    continue;
                }
                if (new HashSet<char>(line.ToCharArray()).Count == 1 && line[0] == '-')
                {
                    Content += "<hr/><br/>" + Environment.NewLine;
                    continue;
                }
                if (rawline.StartsWith("  ", StringComparison.Ordinal))
                {
                    int i = 0;
                    while (i < rawline.Length && rawline[i] == ' ')
                        i++;
                    addline = Fancy.Times("&nbsp;", i) + rawline.TrimStart();
                }
                if (rawline[0] == '*')
                    addline = '•' + addline.Substring(1);
                Content += addline + "<br/>";
            }
            while (Content.Contains("[["))
            {
                int beg = Content.IndexOf("[[", StringComparison.Ordinal);
                int end = Content.IndexOf("]]", StringComparison.Ordinal);
                if (beg < 0 || end < 0 || end < beg)
                {
                    Logger.Log($"Call '{filename}' broken w.r.t. metabrackets");
                    return;
                }
                string before = Content.Substring(0, beg);
                string inside = Content.Substring(beg + 2, end - beg - 2);
                string after = Content.Substring(end + 2);
                string target, text;
                var split = inside.Split('|');
                if (split.Length == 1)
                {
                    target = inside;
                    text = inside;
                }
                else if (split.Length == 2)
                {
                    target = split[0];
                    text = split[1];
                }
                else
                {
                    Logger.Log($"Call '{filename}' broken w.r.t. pipelines");
                    return;
                }

                // [[X]]s
                while (after.Length > 0 && Char.IsLetter(after[0]))
                {
                    text += after[0];
                    after = after.Substring(1);
                }

                // linkification
                if (String.IsNullOrEmpty(target) || String.IsNullOrEmpty(text))
                {
                    Logger.Log($"Call '{filename}' broken w.r.t. metalinks");
                    return;
                }

                if (target.StartsWith("http", StringComparison.Ordinal))
                {
                    inside = $"<a href=\"{target}\">{text}</a>";
                }
                else if (target[0] == '@')
                {
                    target = target.Substring(1);
                    if (text[0] == '@')
                        text = text.Substring(1);
                    inside = $"<a href=\"../person/{Fancy.DeUmlautify(target.Replace(' ', '_'))}.html\">{text}</a>";
                }
                else if (target[0] == '#')
                {
                    target = target.Substring(1).ToLower();
                    if (text[0] == '#')
                        text = text.Substring(1);
                    inside = $"<a href=\"../tag/{target}.html\">{text}</a>";
                }
                else
                {
                    inside = $"<a href=\"../{target}.html\">{text}</a>";
                    //Logger.Log($"Call '{filename}' contvains unintelligible metabracket '{inside}'");
                }

                // get it back together
                Content = before + inside + after;
            }
        }

        public override string ToString()
            => Content;
    }
}
