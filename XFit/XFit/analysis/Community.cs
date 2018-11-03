using System;
using System.Collections.Generic;
using System.Linq;
using XFit.ast;
using XFit.io;
using XFit.refine;

namespace XFit.analysis
{
    internal class Community : CorpusVisitor
    {
        private string venue;

        public SortedSet<string> AllAuthors = new SortedSet<string>();
        public SortedSet<string> AllWords = new SortedSet<string>();
        public SortedSet<string> AllTags = new SortedSet<string>();

        // rel[str venue, rel[str author, int times]]
        public Dictionary<string, Dictionary<string, int>> AuthorDict = new Dictionary<string, Dictionary<string, int>>();

        // rel[str venue, rel[str word, int times]]
        public Dictionary<string, Dictionary<string, int>> VocabDict = new Dictionary<string, Dictionary<string, int>>();

        // rel[str venue, rel[str tag, int times]]
        public Dictionary<string, Dictionary<string, int>> TagDict = new Dictionary<string, Dictionary<string, int>>();

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
            venue = conference.venue;
            if (String.IsNullOrEmpty(venue))
                return false;
            if (!AuthorDict.ContainsKey(venue))
                AuthorDict[venue] = new Dictionary<string, int>();
            if (!VocabDict.ContainsKey(venue))
                VocabDict[venue] = new Dictionary<string, int>();
            if (!TagDict.ContainsKey(venue))
                TagDict[venue] = new Dictionary<string, int>();
            return true;
        }

        public override void ExitConference(Conference conference)
        {
        }

        public override void VisitPaper(Paper paper)
        {
            if (paper.author == null)
                Logger.Log($"Paper {Walker.PureName(paper)} lacks any authors!");
            else
                foreach (string a in paper.author)
                {
                    AllAuthors.Add(a);
                    if (AuthorDict[venue].ContainsKey(a))
                        AuthorDict[venue][a]++;
                    else
                        AuthorDict[venue][a] = 1;
                }
            if (paper.stemmed == null)
                Logger.Log($"Paper {Walker.PureName(paper)} is not stemmed!");
            else
                foreach (string w in paper.stemmed)
                {
                    AllWords.Add(w);
                    if (VocabDict[venue].ContainsKey(w))
                        VocabDict[venue][w]++;
                    else
                        VocabDict[venue][w] = 1;
                }
            if (paper.tag != null) // it's bad to have papers without any tags, but not impossible
            {
                foreach (string t in paper.tag)
                {
                    AllTags.Add(t);
                    if (TagDict[venue].ContainsKey(t))
                        TagDict[venue][t]++;
                    else
                        TagDict[venue][t] = 1;
                }
            }
        }

        public IEnumerable<string> GetVenues()
            => AuthorDict.Keys;

        public Dictionary<string, int> GetQuantified(string venue)
            => !AuthorDict.ContainsKey(venue)
            ? new Dictionary<string, int>()
            : AuthorDict[venue];

        public List<string> GetFlat(string venue)
            => GetQuantified(venue).Keys.ToList();
    }
}
