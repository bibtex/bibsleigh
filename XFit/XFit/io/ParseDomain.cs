using XFit.ast;

namespace XFit.io
{
    public static partial class Parser
    {
        private static void ParseDomain(string path, dynamic input, Domain output)
        {
            //output.Name = input.name;
            //output.Title = input.title;
            //output.Venue = input.venue;
            //ParseDictStrInt(input.tagged, output.Tagged);
            //output.EventUrl = input.eventurl;
            AddBrandsAndYears(Walker.DropExtension(path), output);
        }

        private static void AddBrandsAndYears(string dirname, Domain output)
        {
            if (Walker.DirExists(dirname))
            {
                foreach (var file in Walker.EveryJSON(dirname))
                    output.AddBrand(file);
                foreach (var file in Walker.EveryDir(dirname))
                    output.AddYear(file);
            }
        }
    }
}
