using Newtonsoft.Json;
using System.Collections.Generic;
using System.IO;
using System.Windows.Controls;

namespace XFit.ast
{
    internal class Domain
    {
        private string Name;
        private Dictionary<string, int> Tagged;
        private string Title;
        private string Venue;
        private string EventUrl;
        private List<string> _tags = new List<string> { "name", "title", "venue", "tagged", "eventurl" };

        internal Domain(TextBlock log, string path)
        {
            dynamic domain = JsonConvert.DeserializeObject(File.ReadAllText(path));
            Name = domain.name;
            Title = domain.title;
            Venue = domain.venue;
            GetTagged(domain.tagged);
            EventUrl = domain.eventurl;

            foreach (var p in domain.Properties())
            {
                var key = p.Name;
                if (!_tags.Contains(key))
                    log.Text
                        = $"Unused key '{key}' in domain '{path}'!"
                        + "\n" + log.Text;
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
