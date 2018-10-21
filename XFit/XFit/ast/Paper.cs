using Newtonsoft.Json;
using System.IO;

namespace XFit.ast
{
    internal class Paper
    {
        private string FileName;
        private Conference Parent;

        public Paper(Conference conference, string file)
        {
            FileName = file;
            Parent = conference;
            dynamic domain = JsonConvert.DeserializeObject(File.ReadAllText(file));
        }
    }
}
