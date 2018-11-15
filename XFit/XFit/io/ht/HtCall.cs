using System;
using System.IO;
using XFit.ast;

namespace XFit.io.ht
{
    internal class HtCall : Fancy
    {
        public HtCall(string rootpath, Call call)
        {
            RelativePath = BackOne;
            Title = call.ReadableName + " call";
            IncludeJQuery = false;
            ActiveMenuItem = MenuItem.Calls;

            var potentialIconName = call.Name.ToLower();
            if (potentialIconName.Contains("-"))
                potentialIconName = potentialIconName.Substring(0, potentialIconName.LastIndexOf('-'));
            if (File.Exists(Path.Combine(rootpath, $"stuff\\{potentialIconName}.png")))
                LeftTopIcon = potentialIconName;
            else
                Logger.Log($"Icon '{potentialIconName}' not found");

            if (!TryIfLinkIsAlive(rootpath, call.Name + ".html"))
                if (!TryIfLinkIsAlive(rootpath, call.Name.Split('-')[0] + ".html"))
                    Logger.Log($"No good link found for '{call.Name}' from the call");

            EditPath = $"calls/{call.Name}.cfp";
            Content = $"<h2><span class=\"ttl\">Call</span> of {call.ReadableName}</h2>"
                + Environment.NewLine
                + call.ToString();
        }

        private bool TryIfLinkIsAlive(string path, string link)
        {
            if (!File.Exists(Path.Combine(path, link)))
                return false;
            LeftTopLink = link;
            return true;
        }
    }
}
