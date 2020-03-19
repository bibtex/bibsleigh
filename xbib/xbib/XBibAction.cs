using System;
using System.Json;

namespace xbib
{
    abstract internal class XBibAction
    {
        abstract internal bool Execute(JsonValue json, JsonValue parent);
    }

    internal class XBibTakeFromParent : XBibAction
    {
        private string Key;

        internal XBibTakeFromParent(string key)
        {
            Key = key;
            Console.WriteLine($"[DEBUG] XBibTakeFromParent of {key} is created");
        }

        internal override bool Execute(JsonValue json, JsonValue parent)
        {
            if (parent.ContainsKey(Key))
            {
                JsonValue old = null;
                if (json.ContainsKey(Key))
                    old = json[Key];
                json[Key] = parent[Key];
                return old != json[Key];
            }
            else
                return false;
        }
    }
}