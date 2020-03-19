using System.Json;

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