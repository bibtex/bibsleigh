using System;
using System.Linq;
using XFit.ast;
using XFit.io;

namespace XFit.refine
{
    public class ProceedingsNamer : CorpusVisitor
    {
        public override bool EnterSleigh(Sleigh sleigh)
            => true;

        public override void ExitSleigh(Sleigh sleigh)
        {
        }

        public override bool EnterDomain(Domain domain)
            => true;

        public override void ExitDomain(Domain domain)
        {
        }

        public override void VisitBrand(Brand brand)
        {
        }

        public override bool EnterYear(Year year)
            => true;

        public override void ExitYear(Year year)
        {
        }

        public override bool EnterConference(Conference conference)
        {
            if (IsWeird(conference.title))
            {
                var newtitle = Normalise(conference.title);
                if (newtitle != conference.title)
                {
                    Xformation action = new XConf(GenConfAction(newtitle));
                    Manager.RegisterAction("Misnamed proceedings", conference, action);
                }
            }
            return false;
        }

        public override void ExitConference(Conference conference)
        {
        }

        public override void VisitPaper(Paper paper)
        {
        }

        private bool IsWeird(string title)
            => !String.IsNullOrEmpty(title) && !HasGoodStart(title);

        private bool HasGoodStart(string title)
            => title.StartsWith("Advanced Lectures of", StringComparison.InvariantCulture) ||
                title.StartsWith("Conference Record of", StringComparison.InvariantCulture) ||
                title.StartsWith("Handbook of", StringComparison.InvariantCulture) ||
                title.StartsWith("Joint Meeting of", StringComparison.InvariantCulture) ||
                title.StartsWith("Papers from", StringComparison.InvariantCulture) ||
                title.StartsWith("Post-proceedings of", StringComparison.InvariantCultureIgnoreCase) ||
                title.StartsWith("Proceedings of", StringComparison.InvariantCulture) ||
                title.StartsWith("Record of", StringComparison.InvariantCulture) ||
                title.StartsWith("Revised Papers of", StringComparison.InvariantCulture) ||
                title.StartsWith("Revised Selected and Invited Papers of", StringComparison.InvariantCulture) ||
                title.StartsWith("Revised Selected Papers of", StringComparison.InvariantCulture) ||
                title.StartsWith("Selected and extended papers from", StringComparison.InvariantCulture) ||
                title.StartsWith("Selected Papers of", StringComparison.InvariantCulture) ||
                title.StartsWith("Selected Revised Papers of", StringComparison.InvariantCulture) ||
                title.StartsWith("Special Issue o", StringComparison.InvariantCultureIgnoreCase) ||
                title.StartsWith("Special Section o", StringComparison.InvariantCultureIgnoreCase) ||
                title.StartsWith("Technical Communications of", StringComparison.InvariantCulture) ||
                title.StartsWith("The Annual Meeting of", StringComparison.InvariantCulture) ||
                title.StartsWith("Tutorial Lectures of", StringComparison.InvariantCulture) ||
                title.StartsWith("Tutorials of", StringComparison.InvariantCulture)
            ;

        public string Normalise(string title)
        {
            string[] commas = title.Split(',').Select(s => s.Trim()).ToArray();
            int i = commas.Length - 1;
            bool success = false;
            if (IsCountry(commas[i]) || IsNumber(commas[i]))
            {
                // the heuristic is to keep going left until we see either something like "PDP 2015"
                i--;
                while (i >= 0)
                {
                    var spaces = commas[i].Split(' ');
                    if (spaces.Length == 2 && IsNumber(spaces[1]) && IsUpper(spaces[0]))
                    {
                        success = true;
                        break;
                    }
                    if (commas[i][commas[i].Length - 1] == ')')
                    {
                        commas[i] = commas[i].Split('(')[0].Trim();
                        i++;
                        success = true;
                        break;
                    }
                    i--;
                }
                if (success)
                {
                    var raw = String.Join(", ", commas.Take(i));
                    if (!HasGoodStart(raw))
                        raw = "Proceedings of the " + raw;
                    return raw;
                }
            }

            //////// 23rd Euromicro International Conference on Parallel, Distributed, and Network-Based Processing, PDP 2015, Turku, Finland, March 4-6, 2015
            //////if (commas.Count() >= 6 && IsNumber(commas.Last()) && IsCountry(commas[commas.Count() - 3]) && IsNumber(commas[commas.Count() - 5].Split(' ').Last()))
            //////    return "Proceedings of the " + String.Join(",", commas.Take(commas.Count() - 5));
            //////// 16th Euromicro International Conference on Parallel, Distributed and Network-Based Processing (PDP 2008), 13-15 February 2008, Toulouse, France
            //////if (commas.Count() >= 4 && IsCountry(commas[commas.Count() - 1]) && commas[commas.Count() - 4].EndsWith(")", StringComparison.Ordinal))
            //////    return "Proceedings of the " + String.Join(",", commas.Take(commas.Count() - 4)).Split('(').First().Trim();
            //////// 4th International Forum on Research and Technology Advances in Digital Libraries (ADL '97), Washington, DC, USA, May 7-9, 1997
            //////if (commas.Count() >= 6 && IsNumber(commas.Last()) && IsCountry(commas[commas.Count() - 3]) && commas[commas.Count() - 6].EndsWith(")", StringComparison.Ordinal))
            //////    return "Proceedings of the " + String.Join(",", commas.Take(commas.Count() - 6)).Split('(').First().Trim();
            Logger.Log($"Failed to unpuzzle '{title}'");
            return title;
        }

        private bool IsUpper(string x)
            => x == x.ToUpper();

        private bool IsNumber(string x)
            => Int32.TryParse(x, out int tmp)
            || (x.Length==3 && x[0]=='\'' && IsNumber(x.Substring(1)));

        private bool IsCountry(string x)
            => new string[] { "Belgium", "France", "Germany", "Greece", "Italy", "Portugal", "Spain", "Sweden", "Switzerland", "The Netherlands", "UK", "USA" }.Contains(x);

        private Func<Conference, Conference> GenConfAction(string title)
            => c =>
            {
                var c2 = Parser.Clone(c);
                c2.title = title;
                return c2;
            };
    }
}
