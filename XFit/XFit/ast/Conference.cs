using System;
using System.Collections.Generic;
using System.IO;
using XFit.io;

namespace XFit.ast
{
    internal class Conference
    {
        private string FileName;
        private string DirName;
        private Year Parent;

        private List<Paper> Papers = new List<Paper>();

        public Conference(Year year, string jsonname, string path)
        {
            FileName = String.IsNullOrEmpty(jsonname) ? String.Empty : jsonname;
            DirName = String.IsNullOrEmpty(path) ? String.Empty : path;
            Parent = year;
            foreach (var file in Walker.Everything(path))
            {
                if (File.Exists(file))
                    Papers.Add(new Paper(this, file));
                else
                    Logger.Log($"File out of place: '{file}'");
            }
        }
    }
}