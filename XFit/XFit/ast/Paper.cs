using Newtonsoft.Json;
using System.IO;

namespace XFit.ast
{
    internal class Paper
    {
        private Conference Parent;

        public Paper(Conference conference, string file)
        {
            this.Parent = conference;
            dynamic domain = JsonConvert.DeserializeObject(File.ReadAllText(file));
        }
    }
}
