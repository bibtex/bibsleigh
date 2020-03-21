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
            if (Config.Debug)
                Console.WriteLine($"[DEBUG] XaInherit of {parkey} as {key} is created");
        }

        internal override bool Execute(JsonValue json, JsonValue parent)
        {
            JsonValue old = WokeJ.GetElementByKey(json, Key);
            JsonValue neu = WokeJ.GetElementByKey(parent, ParentKey);
            if (neu != null)
            {
                WokeJ.AddKeyValue(json, Key, neu);
                return WokeJ.GetElementByKey(json, Key) != old;
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
            if (Config.Debug)
                Console.WriteLine($"[DEBUG] XaRemove of {key} is created");
        }

        internal override bool Execute(JsonValue json, JsonValue parent)
        {
            JsonValue old = WokeJ.GetElementByKey(json, Key);
            if (old == null)
                return false;
            (json as JsonObject).Remove(Key);
            return true;
        }
    }

    internal class XaAssign : XbAction
    {
        private string Key;
        private string Value;

        internal XaAssign(string key, string v)
        {
            Key = key;
            Value = v;
            if (Config.Debug)
                Console.WriteLine($"[DEBUG] XaAssign of {key} with '{v}' is created");
        }

        internal override bool Execute(JsonValue json, JsonValue parent)
        {
            JsonValue old = WokeJ.GetElementByKey(json, Key);
            if (Value[0] == '$')
                return _assign(old, json, parent, Key, IO.BareValue(WokeJ.GetElementByKey(json, Value.Substring(1))));
            else
                return _assign(old, json, parent, Key, Value);
        }

        private static bool _assign(JsonValue old, JsonValue json, JsonValue parent, string key, string value)
        {
            if (String.IsNullOrEmpty(value))
                return false;
            if (old != null && old is JsonPrimitive oldP)
            {
                var oldVal = IO.BareValue(oldP);
                json[key] = new JsonPrimitive(value);
                return oldVal != value;
            }
            else
            {
                json[key] = new JsonPrimitive(value);
                return true;
            }
        }
    }

    internal class XaTruncateLeft : XbAction
    {
        private string Key;
        private int Size;

        internal XaTruncateLeft(string key, int x)
        {
            Key = key;
            Size = x;
        }

        internal override bool Execute(JsonValue json, JsonValue parent)
        {
            JsonValue old = WokeJ.GetElementByKey(json, Key);
            if (old == null)
                return false;
            if (old is JsonPrimitive oldP)
            {
                var val = IO.BareValue(oldP);
                if (val.Length >= Size)
                    val = val.Substring(Size);
                json[Key] = new JsonPrimitive(val);
                return old != json[Key];
            }
            else if (old is JsonArray oldA)
            {
                WokeJ.ForAllElements(oldA, e => Execute(e, parent));
                return true; // overapproximation
            }
            else
            if (Config.Debug)
                Console.WriteLine($"[ERROR] Cannot truncate a dictionary, skipped");
            return false;
        }
    }

    internal class XaTruncateRight : XbAction
    {
        private string Key;
        private int Size;

        internal XaTruncateRight(string key, int x)
        {
            Key = key;
            Size = x;
        }

        internal override bool Execute(JsonValue json, JsonValue parent)
        {
            JsonValue old = WokeJ.GetElementByKey(json, Key);
            if (old == null)
                return false;
            if (old is JsonPrimitive oldP)
            {
                var val = IO.BareValue(oldP);
                if (val.Length >= Size)
                    val = val.Substring(0, val.Length - Size);
                json[Key] = new JsonPrimitive(val);
                return old != json[Key];
            }
            else if (old is JsonArray oldA)
            {
                WokeJ.ForAllElements(oldA, e => Execute(e, parent));
                return true; // overapproximation
            }
            else
            if (Config.Debug)
                Console.WriteLine($"[ERROR] Cannot truncate a dictionary, skipped");
            return false;
        }
    }

    internal class XaRenameTo : XbAction
    {
        private string KeyOld;
        private string KeyNew;

        internal XaRenameTo(string oldkey, string newkey)
        {
            KeyOld = oldkey;
            KeyNew = newkey;
        }

        internal override bool Execute(JsonValue json_, JsonValue parent)
        {
            var json = json_ as JsonObject;
            if (json == null)
            {
                if (Config.Debug)
                    Console.WriteLine("[ERROR] Cannot rename something outside a dictionary");
                return false;
            }
            var old = WokeJ.GetElementByKey(json, KeyOld);
            if (old == null)
                return false;
            WokeJ.AddKeyValue(json, KeyNew, old);
            json.Remove(KeyOld);
            return true; // overapptoximation
        }
    }
}