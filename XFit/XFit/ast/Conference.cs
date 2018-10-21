using System.Collections.Generic;
using System.IO;
using XFit.io;

namespace XFit.ast
{
    internal class Conference
    {
        private Year Parent;

        private List<Paper> Papers = new List<Paper>();

        public Conference(Year year, string jsonname, string path)
        {
            this.Parent = year;
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