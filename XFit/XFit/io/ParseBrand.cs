using Newtonsoft.Json.Linq;
using XFit.ast;

namespace XFit.io
{
    internal static partial class Parser
    {
        private static void ParseBrand(string path, dynamic input, Brand output)
        {
            // collocations
            output.Name = input.name;
            if (input.select is JValue sel)
            {
                output.Selected.Clear();
                output.Selected.Add((string)sel);
            }
            else
                ParseListStr(input.select, output.Selected);
            ParseDictStrInt(input.tagged, output.Tagged);
            output.Title = input.title;
            output.Twitter = input.twitter;
            output.DblpKey = input.dblpkey;
            output.DblpUrl = input.dblpurl;
            ParseFlatDictStrInt(input.vocabulary, output.Vocabulary);
        }
    }
}
