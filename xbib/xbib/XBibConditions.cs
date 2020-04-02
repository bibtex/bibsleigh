using System;
using System.Json;

namespace xbib
{
    abstract internal class XbCondition
    {
        abstract internal bool EvaluateB(JsonValue json, JsonValue parent);

        abstract internal bool EvaluateE(JsonPrimitive jp, JsonValue json, JsonValue parent);

        abstract internal string GetContext();
    }

    internal class XcConjunction : XbCondition
    {
        private XbCondition X, Y;

        internal XcConjunction(XbCondition left, XbCondition right)
        {
            X = left;
            Y = right;
        }

        internal override bool EvaluateB(JsonValue json, JsonValue parent)
            => X.EvaluateB(json, parent)
            && Y.EvaluateB(json, parent);

        internal override bool EvaluateE(JsonPrimitive jp, JsonValue json, JsonValue parent)
            => X.EvaluateE(jp, json, parent)
            && Y.EvaluateE(jp, json, parent);

        internal override string GetContext()
            => Y.GetContext();
    }

    internal class XcExistsKey : XbCondition
    {
        private string Key;

        internal XcExistsKey(string key)
        {
            Key = key;
            if (Config.Debug)
                Console.WriteLine($"[DEBUG] XBibExistsKey of {key} is created");
        }

        internal override bool EvaluateB(JsonValue json, JsonValue parent)
            => json.ContainsKey(Key);

        internal override bool EvaluateE(JsonPrimitive jp, JsonValue json, JsonValue parent)
        {
            throw new NotImplementedException();
        }

        internal override string GetContext()
            => Key;
    }

    internal class XcNegation : XbCondition
    {
        private XbCondition Inner;

        internal XcNegation(XbCondition cond)
        {
            Inner = cond;
            if (Config.Debug)
                Console.WriteLine($"[DEBUG] XcNegation of {cond} is created");
        }

        internal override bool EvaluateB(JsonValue json, JsonValue parent)
            => !Inner.EvaluateB(json, parent);

        internal override bool EvaluateE(JsonPrimitive jp, JsonValue json, JsonValue parent)
            => !Inner.EvaluateE(jp, json, parent);

        internal override string GetContext()
            => Inner.GetContext();
    }

    internal class XcMatchesExactly : XbCondition
    {
        private string Key;
        private string Value;
        private string OtherKey;

        internal XcMatchesExactly(string key, string val)
        {
            Key = key;
            if (val[0] == '$')
            {
                Value = null;
                OtherKey = val.Substring(1);
            }
            else
            {
                Value = val;
                OtherKey = null;
            }
            if (Config.Debug)
                Console.WriteLine($"[DEBUG] XcMatchesExactly of {key} with '{val}' is created");
        }

        internal override bool EvaluateB(JsonValue json, JsonValue parent)
            => json.ContainsKey(Key)
            && json[Key] is JsonPrimitive jp
            && EvaluateE(jp, json, parent);

        internal override bool EvaluateE(JsonPrimitive jp, JsonValue json, JsonValue parent)
            => String.IsNullOrEmpty(Value)
            ? json.ContainsKey(OtherKey) && IO.BareValue(jp) == IO.BareValue(json[OtherKey])
            : IO.BareValue(jp) == Value;

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
            if (Config.Debug)
                Console.WriteLine($"[DEBUG] XcMatchesParentExactly of {key1} with ^{key2} is created");
        }

        internal override bool EvaluateB(JsonValue json, JsonValue parent)
            => parent != null
            && json.ContainsKey(Key)
            && json[Key] is JsonPrimitive jp
            && EvaluateE(jp, json, parent);

        internal override bool EvaluateE(JsonPrimitive jp, JsonValue json, JsonValue parent)
            => parent.ContainsKey(ParentKey)
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
            if (Config.Debug)
                Console.WriteLine($"[DEBUG] XcMatchesLeft of {key} with '{val}' is created");
        }

        internal override bool EvaluateB(JsonValue json, JsonValue parent)
            => json.ContainsKey(Key)
            && json[Key] is JsonPrimitive jp
            && EvaluateE(jp, json, parent);

        internal override bool EvaluateE(JsonPrimitive jp, JsonValue json, JsonValue parent)
            => IO.BareValue(jp).StartsWith(Value);

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
            if (Config.Debug)
                Console.WriteLine($"[DEBUG] XcMatchesRight of {key} with '{val}' is created");
        }

        internal override bool EvaluateB(JsonValue json, JsonValue parent)
            => json.ContainsKey(Key)
            && json[Key] is JsonPrimitive jp
            && EvaluateE(jp, json, parent);

        internal override bool EvaluateE(JsonPrimitive jp, JsonValue json, JsonValue parent)
            => IO.BareValue(jp).EndsWith(Value);

        internal override string GetContext()
            => Key;
    }

    internal class XcAlways : XbCondition
    {
        internal override bool EvaluateB(JsonValue json, JsonValue parent)
            => true;

        internal override bool EvaluateE(JsonPrimitive jp, JsonValue json, JsonValue parent)
            => true;

        internal override string GetContext()
            => String.Empty;
    }
}