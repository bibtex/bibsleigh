﻿using System;
using System.Json;

namespace xbib
{
    abstract internal class XbCondition
    {
        abstract internal bool Evaluate(JsonValue json, JsonValue parent);

        abstract internal string GetContext();
    }

    internal class XcExistsKey : XbCondition
    {
        private string Key;

        internal XcExistsKey(string key)
        {
            Key = key;
            Console.WriteLine($"[DEBUG] XBibExistsKey of {key} is created");
        }

        internal override bool Evaluate(JsonValue json, JsonValue parent)
            => json.ContainsKey(Key);

        internal override string GetContext()
            => Key;
    }

    internal class XcNegation : XbCondition
    {
        private XbCondition Inner;

        internal XcNegation(XbCondition cond)
        {
            Inner = cond;
            Console.WriteLine($"[DEBUG] XcNegation of {cond} is created");
        }

        internal override bool Evaluate(JsonValue json, JsonValue parent)
            => !Inner.Evaluate(json, parent);

        internal override string GetContext()
            => Inner.GetContext();
    }

    internal class XcMatchesExactly : XbCondition
    {
        private string Key;
        private string Value;

        internal XcMatchesExactly(string key, string val)
        {
            Key = key;
            Value = val;
            Console.WriteLine($"[DEBUG] XcMatchesExactly of {key} with '{val}' is created");
        }

        internal override bool Evaluate(JsonValue json, JsonValue parent)
            => json.ContainsKey(Key)
            && json[Key] is JsonPrimitive jp
            && IO.BareValue(jp) == Value;

        internal override string GetContext()
            => Key;
    }

    internal class XcMatchesParentExactly : XbCondition
    {
        private string Key;
        private string ParentKey;

        internal XcMatchesParentExactly(string key1, string key2)
        {
            Key = key1;
            ParentKey = key2;
            Console.WriteLine($"[DEBUG] XcMatchesParentExactly of {key1} with ^{key2} is created");
        }

        internal override bool Evaluate(JsonValue json, JsonValue parent)
            => parent != null
            && json.ContainsKey(Key)
            && json[Key] is JsonPrimitive jp
            && parent.ContainsKey(ParentKey)
            && parent[ParentKey] is JsonPrimitive jpp
            && IO.BareValue(jp) == IO.BareValue(jpp);

        internal override string GetContext()
            => Key;
    }

    internal class XcMatchesLeft : XbCondition
    {
        private string Key;
        private string Value;

        internal XcMatchesLeft(string key, string val)
        {
            Key = key;
            Value = val;
            Console.WriteLine($"[DEBUG] XcMatchesLeft of {key} with '{val}' is created");
        }

        internal override bool Evaluate(JsonValue json, JsonValue parent)
            => json.ContainsKey(Key)
            && json[Key] is JsonPrimitive jp
            && IO.BareValue(jp).StartsWith(Value);

        internal override string GetContext()
            => Key;
    }

    internal class XcMatchesRight : XbCondition
    {
        private string Key;
        private string Value;

        internal XcMatchesRight(string key, string val)
        {
            Key = key;
            Value = val;
            Console.WriteLine($"[DEBUG] XcMatchesRight of {key} with '{val}' is created");
        }

        internal override bool Evaluate(JsonValue json, JsonValue parent)
            => json.ContainsKey(Key)
            && json[Key] is JsonPrimitive jp
            && IO.BareValue(jp).EndsWith(Value);

        internal override string GetContext()
            => Key;
    }
}