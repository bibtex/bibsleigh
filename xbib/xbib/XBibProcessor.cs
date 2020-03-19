using System;
using System.Collections.Generic;
using System.IO;

namespace xbib
{
    internal class XBibProcessor
    {
        private string Corpus;

        private List<XBibRule> Rules = new List<XBibRule>();

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
                else if (line.StartsWith("in ") && i + 2 < text.Length)
                {
                    string s1, s2, s3;
                    s1 = CuratePath(line.Substring(3).Trim());
                    s2 = text[i + 1].Trim();
                    s3 = text[i + 2].Trim();
                    if (s2.StartsWith("when") && s3.StartsWith("take"))
                        Rules.Add(new InWhenTake(s1, s2, s3));
                    else 
                        throw new NotImplementedException("wrong xbib command: " + line);
                    i += 3;
                }
                else
                    throw new NotImplementedException("wrong xbib command: " + line);
            }
        }

        internal void Engage()
        {
            if (String.IsNullOrEmpty(Corpus))
                Corpus = Directory.GetCurrentDirectory();
            DirectoryInfo root = new DirectoryInfo(Corpus);

            foreach (var rule in Rules)
                rule.Enforce(root);
        }

        private void AssignCorpus(string c)
        {
            if (Directory.Exists(c))
                Corpus = c;
            else
                throw new IOException($"corpus '{c}' not found");
        }

        private string CuratePath(string p)
            => p.Replace("/", "\\");
    }
}