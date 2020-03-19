using System;
using System.Json;

namespace xbib
{
    abstract internal class XBibCondition
    {
        abstract internal bool Evaluate(JsonValue json);
        abstract internal string GetContext();
    }

    internal class XBibExistsKey : XBibCondition
    {
        private string Key;

        internal XBibExistsKey(string key)
        {
            Key = key;
            Console.WriteLine($"[DEBUG] XBibExistsKey of {key} is created");
        }

        internal override bool Evaluate(JsonValue json)
            => json.ContainsKey(Key);

        internal override string GetContext()
            => Key;
    }

    internal class XBibNegation : XBibCondition
    {
        private XBibCondition Inner;

        internal XBibNegation(XBibCondition cond)
        {
            Inner = cond;
            Console.WriteLine($"[DEBUG] XBibNegation of {cond} is created");
        }

        internal override bool Evaluate(JsonValue json)
            => !Inner.Evaluate(json);

        internal override string GetContext()
            => Inner.GetContext();
    }
}