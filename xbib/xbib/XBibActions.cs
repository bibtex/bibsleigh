using System;
using System.Json;

namespace xbib
{
    abstract internal class XbAction
    {
        abstract internal bool Execute(JsonValue json, JsonValue parent);
    }

    internal class XaInherit : XbAction
    {
        private string Key;
        private string ParentKey;

        internal XaInherit(string key, string parkey)
        {
            Key = key;
            ParentKey = parkey;
            Console.WriteLine($"[DEBUG] XaInherit of {parkey} as {key} is created");
        }

        internal override bool Execute(JsonValue json, JsonValue parent)
        {
            if (parent.ContainsKey(ParentKey))
            {
                JsonValue old = null;
                if (json.ContainsKey(Key))
                    old = json[Key];
                json[Key] = parent[ParentKey];
                return old != json[Key];
            }
            else
                return false;
        }
    }

    internal class XaRemove : XbAction
    {
        private string Key;

        internal XaRemove(string key)
        {
            Key = key;
            Console.WriteLine($"[DEBUG] XaRemove of {key} is created");
        }

        internal override bool Execute(JsonValue json, JsonValue parent)
        {
            JsonObject json2 = json as JsonObject;
            if (json2 != null && json2.ContainsKey(Key))
            {
                json2.Remove(Key);
                return true;
            }
            return false;
        }
    }
}