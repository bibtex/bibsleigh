using System;
using System.Json;
using System.Linq;

namespace xbib
{
    abstract internal class XbAction
    {
        abstract internal bool ExecuteB(JsonObject json, JsonObject parent);

        abstract internal JsonPrimitive ExecuteE(JsonPrimitive jp, JsonValue json, JsonValue parent);
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

        internal override bool ExecuteB(JsonObject json, JsonObject parent)
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

        internal override JsonPrimitive ExecuteE(JsonPrimitive jp, JsonValue json, JsonValue parent)
        {
            throw new NotImplementedException();
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

        internal override bool ExecuteB(JsonObject json, JsonObject parent)
        {
            JsonValue old = WokeJ.GetElementByKey(json, Key);
            if (old == null)
                return false;
            json.Remove(Key);
            return true;
        }

        internal override JsonPrimitive ExecuteE(JsonPrimitive jp, JsonValue json, JsonValue parent)
            => null;
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

        internal override bool ExecuteB(JsonObject json, JsonObject parent)
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

        internal override JsonPrimitive ExecuteE(JsonPrimitive jp, JsonValue json, JsonValue parent)
        {
            if (Value[0] == '$')
                return new JsonPrimitive(IO.BareValue(WokeJ.GetElementByKey(json, Value.Substring(1))));
            else
                return new JsonPrimitive(Value);
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

        internal override bool ExecuteB(JsonObject json, JsonObject parent)
        {
            JsonValue old = WokeJ.GetElementByKey(json, Key);
            if (old == null)
                return false;
            if (old is JsonPrimitive oldP)
            {
                json[Key] = ExecuteE(oldP, json, parent);
                return old != json[Key];
            }
            else if (old is JsonArray oldA)
            {
                Console.WriteLine($"got to the array {oldA}");
                WokeJ.MapReduce(oldA, e => e is JsonPrimitive ep ? ExecuteE(ep, json, parent) : e);
                return true; // overapproximation
            }
            else
            if (Config.Debug)
                Console.WriteLine($"[ERROR] Cannot truncate a dictionary, skipped");
            return false;
        }

        internal override JsonPrimitive ExecuteE(JsonPrimitive jp, JsonValue json, JsonValue parent)
        {
            var val = IO.BareValue(jp);
            if (val.Length >= Size)
                val = val.Substring(Size);
            return new JsonPrimitive(val);
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

        internal override bool ExecuteB(JsonObject json, JsonObject parent)
        {
            JsonValue old = WokeJ.GetElementByKey(json, Key);
            if (old == null)
                return false;
            if (old is JsonPrimitive oldP)
            {
                json[Key] = ExecuteE(oldP, json, parent);
                return old != json[Key];
            }
            else if (old is JsonArray oldA)
            {
                // TODO
                return false;
                //WokeJ.ForAllElements(oldA, e => ExecuteB(e, parent));
                //return true; // overapproximation
            }
            else
            if (Config.Debug)
                Console.WriteLine($"[ERROR] Cannot truncate a dictionary, skipped");
            return false;
        }

        internal override JsonPrimitive ExecuteE(JsonPrimitive jp, JsonValue json, JsonValue parent)
        {
            var val = IO.BareValue(jp);
            if (val.Length >= Size)
                val = val.Substring(0, val.Length - Size);
            return new JsonPrimitive(val);
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

        internal override bool ExecuteB(JsonObject json, JsonObject parent)
        {
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

        internal override JsonPrimitive ExecuteE(JsonPrimitive jp, JsonValue json, JsonValue parent)
        {
            if (json == null)
            {
                if (Config.Debug)
                    Console.WriteLine("[ERROR] Cannot rename something outside a dictionary");
                return jp;
            }
            WokeJ.AddKeyValue(json, KeyNew, jp);
            return null;
        }
    }

    internal class XaTouch : XbAction
    {
        internal override bool ExecuteB(JsonObject json, JsonObject parent)
        {
            bool changed = false;
            foreach (var k in json.Keys.ToList())
            {
                if (json[k] is JsonPrimitive jp)
                {
                    var s = jp.ToString();
                    if (s.Length < 3 || s[0] != '"' || s[s.Length - 1] != '"')
                        continue;
                    s = s.Substring(1, s.Length - 2);

                    if (k == "journal" && s.Length < 10)
                        Console.WriteLine($"Strange journal name in {json["title"]} : '{s}'");
                    if (k == "booktitle" && s.Length < 10)
                        Console.WriteLine($"Strange book name in {json["title"]} : '{s}'");
                    if (Int32.TryParse(s, out int n))
                    {
                        json[k] = new JsonPrimitive(n);
                        changed = true;
                    }
                    else if (k == "booktitle" && s.Length > 5)
                    {
                        foreach (var wrong in Constants.Numerals.Keys)
                            if (s.IndexOf(wrong) > 0)
                            {
                                json[k] = new JsonPrimitive(s.Replace(wrong, Constants.Numerals[wrong]));
                                changed = true;
                                break;
                            }
                    }
                }
            }
            return changed;
        }

        internal override JsonPrimitive ExecuteE(JsonPrimitive jp, JsonValue json, JsonValue parent)
            => jp;
    }
}