using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Controls;
using XFit.ast;
using XFit.io;

namespace XFit.analysis
{
    internal class Recommender
    {
        public int Count => Files == null ? 0 : Files.Count();
        public string Name { get; private set; }
        public List<string> Files { get; private set; }
        private Dictionary<string, Xformation> plan = new Dictionary<string, Xformation>();
        private Dictionary<string, Serialisable> input = new Dictionary<string, Serialisable>();

        internal Recommender(string name)
        {
            Name = name;
            Files = new List<string>();
        }

        internal void Add(Serialisable before, Xformation action)
        {
            string file = before.FileName;
            plan[file] = action;
            input[file] = before;
            Files.Add(file);
        }

        internal Xformation Get(string file)
            => plan.ContainsKey(file)
            ? plan[file]
            : null;

        internal void HighlightFile(int index, TextBox before, TextBox after)
        {
            string file = Files[index];
            Logger.Log($"highlight '{file}'");
            before.Text = Parser.Unparse(input[file]);
            after.Text = Parser.Unparse(plan[file].Transform(input[file]));
        }
    }
}
