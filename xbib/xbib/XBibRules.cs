using System.Json;

namespace xbib
{
    internal abstract class XBibRule
    {
        internal abstract bool Enforce(JsonValue json, JsonValue parent);
    }

    internal class XBibGuardedAction : XBibRule
    {
        private XBibCondition Guard;
        private XBibAction Act;

        internal XBibGuardedAction(string cond, string act)
        {
            Guard = XBibParser.ParseCondition(cond);
            Act = XBibParser.ParseAction(act, Guard.GetContext());
        }

        internal override bool Enforce(JsonValue json, JsonValue parent)
        {
            if (Guard.Evaluate(json))
                return Act.Execute(json, parent);
            else
                return false;
        }
    }
}