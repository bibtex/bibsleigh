using System;
using System.Collections.Generic;
using System.IO;
using System.Json;

namespace xbib
{
    internal class XBibProcessor
    {
        private const string PathToPaper = @"*\*\*\*";
        private const string PathToConf = @"*\*\*";

        private string Corpus;
        private string ThePath;

        private Dictionary<string, List<XbRule>> Rules = new Dictionary<string, List<XbRule>>();

        internal XBibProcessor(string filename)
        {
            Rules[PathToPaper] = new List<XbRule>();
            Rules[PathToConf] = new List<XbRule>();

            string[] text = File.ReadAllLines(CuratePath(filename));
            int i = 0;
            string line;
            while (i < text.Length)
            {
                line = text[i].Trim();
                if (String.IsNullOrEmpty(line)) // empty line
                    i++;
                else if (line.StartsWith("--")) // comment
                    i++;
                else if (line.StartsWith("corpus "))
                {
                    AssignCorpus(CuratePath(line.Substring(7).Trim()));
                    i++;
                }
                else if (line.StartsWith("in "))
                {
                    AssignPath(CuratePath(line.Substring(3).Trim()));
                    i++;
                }
                else
                {
                    var rule = IO.ParseRule(line, text, ref i);
                    if (rule != null)
                        Rules[ThePath].Add(rule);
                }
            }
        }

        internal void Engage()
        {
            if (String.IsNullOrEmpty(Corpus))
                Corpus = Directory.GetCurrentDirectory();
            DirectoryInfo root = new DirectoryInfo(Corpus);
            EnforceInLeaves(root);
        }

        private void EnforceInLeaves(DirectoryInfo corpus)
        {
            foreach (var unoF in corpus.GetDirectories("*"))
                foreach (var duoF in unoF.GetDirectories("*"))
                {
                    Dictionary<string, JsonValue> PossibleParents = new Dictionary<string, JsonValue>();
                    foreach (var treJ in duoF.GetFiles("*.json"))
                    {
                        var json = WokeJ.ParseJson(treJ.FullName);
                        bool changed = false;
                        foreach (var rule in Rules[PathToConf])
                            changed |= rule.Enforce(json, null); // TODO: parents of conferences
                        if (changed)
                        {
                            File.WriteAllText(treJ.FullName, WokeJ.UnParseJson(json));
                            //Console.WriteLine(XBibParser.UnParseJson(json));
                            //throw new Exception();
                            Console.WriteLine($"Updated {unoF}/{duoF}/{treJ}");
                        }
                        PossibleParents[Path.GetFileNameWithoutExtension(treJ.Name)] = json;
                    }
                    foreach (var treF in duoF.GetDirectories("*"))
                    {
                        int i = 0, j = 0;
                        JsonValue Parent = null;
                        if (PossibleParents.ContainsKey(treF.Name))
                            Parent = PossibleParents[treF.Name];
                        foreach (var quaJ in treF.GetFiles("*.json"))
                        {
                            JsonValue json = WokeJ.ParseJson(quaJ.FullName);
                            if (json == null)
                                continue;
                            bool changed = false;
                            foreach (var rule in Rules[PathToPaper])
                                changed |= rule.Enforce(json, Parent);
                            if (changed)
                            {
                                //Console.WriteLine("qapla!");
                                File.WriteAllText(quaJ.FullName, WokeJ.UnParseJson(json));
                                //Console.WriteLine(XBibParser.UnParseJson(json));
                                //throw new Exception();
                                j++;
                            }
                            i++;
                        }
                        if (j > 0)
                            Console.WriteLine($"{unoF.Name}/{duoF.Name}/{treF.Name}: {i} entries{(Parent == null ? "" : " + parent")} - {j} updated");
                    }
                }
        }

        private void AssignCorpus(string c)
        {
            if (Directory.Exists(c))
                Corpus = c;
            else
                throw new IOException($"corpus '{c}' not found");
        }

        private void AssignPath(string p)
        {
            ThePath = p;
            if (!Rules.ContainsKey(ThePath))
            {
                Rules[ThePath] = new List<XbRule>();
                Console.WriteLine($"[WARN] Suspiciously unfamiliar path: '{ThePath}' (know {String.Join(" and ", Rules.Keys)})");
            }
        }

        private string CuratePath(string p)
            => p.Replace("/", "\\");
    }
}