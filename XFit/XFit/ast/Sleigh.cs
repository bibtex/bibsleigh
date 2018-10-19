﻿using System.Collections.Generic;
using System.IO;
using System.Windows.Controls;

namespace XFit.ast
{
    internal class Sleigh
    {
        private List<Domain> Domains = new List<Domain>();

        internal Sleigh(TextBlock log, string path)
        {
            foreach (var domainFile in Directory.GetFiles(path, "*.json", SearchOption.TopDirectoryOnly))
            {
                Domains.Add(new Domain(log, domainFile));
            }
        }

        public int NoOfDomains
        {
            get => Domains.Count;
        }
    }
}
