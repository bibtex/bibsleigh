using XFit.ast;

namespace XFit.io
{
    internal static partial class Parser
    {
        private static void ParseDomain(string path, dynamic domain, Domain output)
        {
            output.Name = domain.name;
            output.Title = domain.title;
            output.Venue = domain.venue;
            ParseDictStrInt(domain.tagged, output.Tagged);
            output.EventUrl = domain.eventurl;
            AddBrandsAndYears(Walker.DropExtension(path), output);
            CheckForUnusedKeys(path, domain.Properties());
        }

        private static void AddBrandsAndYears(string dirname, Domain output)
        {
            if (Walker.DirExists(dirname))
                foreach (var file in Walker.Everything(dirname))
                    if (Walker.FileExists(file))
                        output.Brands.Add(new Brand(output, file));
                    else if (Walker.DirExists(file))
                        output.Years.Add(new Year(output, file));
        }
    }
}
