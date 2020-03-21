using System;
using System.Collections.Generic;
using System.Json;
using System.Linq;

namespace xbib
{
    internal abstract class XbRule
    {
        internal abstract bool Enforce(JsonValue json, JsonValue parent);
    }

    internal class XrGuardedAction : XbRule
    {
        private XbCondition Guard;
        private XbAction Act;

        public XrGuardedAction(XbCondition guard, XbAction act)
        {
            Guard = guard;
            Act = act;
            if (Config.Debug)
                Console.WriteLine($"[DEBUG] XrGuardedAction of {Guard} => {Act}");
        }

        internal override bool Enforce(JsonValue json, JsonValue parent)
        {
            if (Guard.EvaluateB(json, parent))
                return Act.ExecuteB(json, parent);
            else
                return false;
        }
    }

    internal class XrIterativeAction : XbRule
    {
        private string Focus;
        private XbCondition Guard;
        private XbAction Act;

        public XrIterativeAction(string focus, XbCondition guard, XbAction act)
        {
            Focus = focus;
            Guard = guard;
            Act = act;
            if (Config.Debug)
                Console.WriteLine($"[DEBUG] XrIterativeAction of {Focus} in {Guard} => {Act}");
        }

        internal override bool Enforce(JsonValue json_, JsonValue parent)
        {
            var json = json_ as JsonObject;
            if (json == null || !json.ContainsKey(Focus))
                return false;
            JsonValue f = json[Focus];
            if (f is JsonPrimitive fp)
            {
                if (Guard.EvaluateE(fp, json, parent))
                {
                    var r = Act.ExecuteE(fp, json, parent);
                    if (r == null)
                    {
                        json.Remove(Focus);
                        return true;
                    }
                    else
                    {
                        json[Focus] = r;
                        return fp == r;
                    }
                }
                else
                    return false;
            }
            else if (f is JsonArray fa)
            {
                List<string> bag = new List<string>();
                for (int i = 0; i < fa.Count; i++)
                {
                    var el = fa[i] as JsonPrimitive;
                    if (el == null)
                    {
                        Console.WriteLine($"Nested structures are not permitted: {fa[i]}");
                        return false;
                    }
                    if (Guard.EvaluateE(el, json, parent))
                    {
                        JsonPrimitive r = Act.ExecuteE(el, json, parent);
                        var v = IO.BareValue(r);
                        if (r != null && !bag.Contains(v))
                            bag.Add(v);
                    }
                    else
                    {
                        if (!bag.Contains(el))
                            bag.Add(IO.BareValue(el));
                    }
                }
                if (bag.Count == 1)
                    json[Focus] = bag[0];
                else
                    json[Focus] = new JsonArray(bag.Select(x => new JsonPrimitive(x)));
                return f != json[Focus];
            }
            else
            {
                Console.WriteLine($"Nested structures are not permitted: {f}");
                return false;
            }
        }
    }
}