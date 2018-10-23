using System;
using System.Collections.Generic;
using System.IO;
using XFit.io;

namespace XFit.ast
{
    public class Conference : Serialisable
    {
        private string FileName;
        private string DirName;
        private Year Parent;

        private List<Paper> Papers = new List<Paper>();

        public Conference(Year year)
        {
            Parent = year;
        }

        public void FromDisk(string path)
        {
            FileName = Path.ChangeExtension(path, "json");
            DirName = path;
            Parser.JSONtoConf(path, this);
        }
        internal void AddPaper(string file)
        {
            Papers.Add(new Paper(this, file));
        }
    }
}
