using Newtonsoft.Json;
using System.Collections.Generic;
using System.IO;

namespace XFit.ast
{
    internal class Domain
    {
        private readonly Sleigh Parent;

        private string Name;
        private Dictionary<string, int> Tagged;
        private string Title;
        private string Venue;
        private string EventUrl;
        private List<Brand> Brands = new List<Brand>();
        private List<Year> Years = new List<Year>();

        private List<string> _tags = new List<string> { "name", "title", "venue", "tagged", "eventurl" };

        internal Domain(Sleigh parent, string path)
        {
            Parent = parent;
            dynamic domain = JsonConvert.DeserializeObject(File.ReadAllText(path));
            Name = domain.name;
            Title = domain.title;
            Venue = domain.venue;
            GetTagged(domain.tagged);
            EventUrl = domain.eventurl;
            var dirname = Path.ChangeExtension(path, "");
            if (Directory.Exists(dirname))
                foreach (var file in Directory.GetFiles(dirname, "*", SearchOption.TopDirectoryOnly))
                    if (File.Exists(file))
                        Brands.Add(new Brand(this, file));
                    else if (Directory.Exists(file))
                        Years.Add(new Year(this, file));

            foreach (var p in domain.Properties())
            {
                var key = p.Name;
                if (!_tags.Contains(key))
                    Logger.Log($"Unused key '{key}' in domain '{path}'!");
            }
        }

        private void GetTagged(dynamic t)
        {
            Tagged = new Dictionary<string, int>();
            if (t == null)
                return;
            foreach (dynamic te in t)
                Tagged[(string)te[0]] = (int)te[1];
        }
    }
}
