using System;
using XFit.ast;
using XFit.io;

namespace XFit.analysis
{
    internal class EmptyVenueFinder : CorpusVisitor
    {
        private string confvenue;

        public override void VisitSleigh(Sleigh sleigh)
        {
        }

        public override void VisitDomain(Domain domain)
        {
        }

        public override void VisitBrand(Brand brand)
        {
        }

        public override void VisitYear(Year year)
        {
        }

        public override void VisitConference(Conference conference)
        {
            if (String.IsNullOrEmpty(conference.venue))
            {
                Logger.Log($"Conference '{Walker.PureName(conference)}' lacks a venue!");
                confvenue = String.Empty;
            }
            else
                confvenue = conference.venue;
        }

        public override void VisitPaper(Paper paper)
        {
            if (!String.IsNullOrEmpty(paper.venue))
                return;
            if (String.IsNullOrEmpty(confvenue))
                Logger.Log($"Paper '{Walker.PureName(paper)}' lacks a venue, buts is parent conference lacks it too!");
            else 
                Logger.Log($"Paper '{Walker.PureName(paper)}' lacks a venue: TODO add an action!");
        }
    }
}
