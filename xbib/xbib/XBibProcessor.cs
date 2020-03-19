using System;
using System.Collections.Generic;
using System.IO;
using System.Json;

namespace xbib
{
    internal class XBibProcessor
    {
        private string Corpus;
        private string ThePath;

        private List<XbRule> Rules = new List<XbRule>();

        internal XBibProcessor(string filename)
        {
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
                    Rules.Add(XBibParser.ParseRule(line, text, ref i));
            }
        }

        internal void Engage()
        {
            if (String.IsNullOrEmpty(Corpus))
                Corpus = Directory.GetCurrentDirectory();
            DirectoryInfo root = new DirectoryInfo(Corpus);

            if (ThePath == @"*\*\*\*")
                EnforceInLeaves(root);
            else
                throw new NotImplementedException($"Path '{ThePath}' unsupported");
        }

        private void EnforceInLeaves(DirectoryInfo corpus)
        {
            foreach (var unoF in corpus.GetDirectories("*"))
                foreach (var duoF in unoF.GetDirectories("*"))
                {
                    Dictionary<string, FileInfo> PossibleParents = new Dictionary<string, FileInfo>();
                    foreach (var treJ in duoF.GetFiles("*.json"))
                        PossibleParents[Path.GetFileNameWithoutExtension(treJ.Name)] = treJ;
                    foreach (var treF in duoF.GetDirectories("*"))
                    {
                        int i = 0, j = 0;
                        JsonValue Parent = null;
                        if (PossibleParents.ContainsKey(treF.Name))
                            Parent = XBibParser.ParseJson(PossibleParents[treF.Name].FullName);
                        foreach (var quaF in treF.GetFiles("*.json"))
                        {
                            JsonValue json = XBibParser.ParseJson(quaF.FullName);
                            if (json == null)
                                continue;
                            bool changed = false;
                            foreach (var rule in Rules)
                                changed |= rule.Enforce(json, Parent);
                            if (changed)
                            {
                                //Console.WriteLine("qapla!");
                                File.WriteAllText(quaF.FullName, XBibParser.UnParseJson(json));
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
        }

        private string CuratePath(string p)
            => p.Replace("/", "\\");
    }
}