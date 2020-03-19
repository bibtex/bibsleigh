using System;
using System.Collections.Generic;
using System.IO;
using System.Json;

namespace xbib
{
    internal abstract class XBibRule
    {
        internal abstract void Enforce(DirectoryInfo corpus);
    }

    internal class InWhenTake : XBibRule
    {
        private string ThePath;
        private XBibCondition Guard;
        private XBibAction Act;

        internal InWhenTake(string path, string cond, string act)
        {
            ThePath = path;
            Guard = XBibParser.ParseCondition(cond);
            Act = XBibParser.ParseAction(act, Guard.GetContext());
        }

        internal override void Enforce(DirectoryInfo corpus)
        {
            if (ThePath == @"*\*\*\*")
                EnforceInLeaves(corpus);
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
                            if (Guard.Evaluate(json))
                            {
                                bool done = Act.Execute(json, Parent);
                                if (done)
                                {
                                    //Console.WriteLine("qapla!");
                                    File.WriteAllText(quaF.FullName, XBibParser.UnParseJson(json));
                                    //Console.WriteLine(XBibParser.UnParseJson(json));
                                    //throw new Exception();
                                    j++;
                                }
                                //else
                                //Console.WriteLine("execute failed");
                            }
                            //else
                            //Console.WriteLine("guard failed");
                            i++;
                        }
                        if (j > 0)
                            Console.WriteLine($"{unoF.Name}/{duoF.Name}/{treF.Name}: {i} entries{(Parent == null ? "" : " + parent")} - {j} fixed");
                    }
                }
        }
    }
}