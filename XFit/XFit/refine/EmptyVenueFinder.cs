using System;
using XFit.ast;
using XFit.io;

namespace XFit.refine
{
    internal class EmptyVenueFinder : CorpusVisitor
    {
        private string confvenue;

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
            if (String.IsNullOrEmpty(conference.venue))
            {
                string proposed = Walker.PureName(conference).Split('-')[0];
                Xformation action = new XConf(GenConfAction(proposed));
                Manager.RegisterAction("Conference lacks a venue", conference, action);
                confvenue = String.Empty;
                return false;
            }
            else
            {
                confvenue = conference.venue;
                return true;
            }
        }

        public override void ExitConference(Conference conference)
        {
            confvenue = String.Empty;
        }

        public override void VisitPaper(Paper paper)
        {
            if (!String.IsNullOrEmpty(paper.venue))
                return;
            if (String.IsNullOrEmpty(confvenue))
                Logger.Log($"Paper '{Walker.PureName(paper)}' lacks a venue, buts is parent conference lacks it too!");
            else
            {
                Xformation action = new XPaper(GenPaperAction(confvenue));
                Manager.RegisterAction("Paper lacks a venue", paper, action);
            }
        }

        private Func<Paper, Paper> GenPaperAction(string venue)
            => p =>
            {
                var p2 = Parser.Clone(p);
                p2.venue = venue;
                return p2;
            };

        private Func<Conference, Conference> GenConfAction(string venue)
            => c =>
            {
                var c2 = Parser.Clone(c);
                c2.venue = venue;
                return c2;
            };
    }
}
