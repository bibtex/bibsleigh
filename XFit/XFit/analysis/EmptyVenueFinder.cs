using System;
using XFit.ast;
using XFit.io;

namespace XFit.analysis
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
                Conference f(Conference c)
                {
                    c.venue = proposed;
                    return c;
                }
                Xformation action = new XConf(f);
                Manager.RegisterAction("Conference lacks a venue", conference, action);
                //Logger.Log($"Conference '{Walker.PureName(conference)}' lacks a venue!");
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
        }

        public override void VisitPaper(Paper paper)
        {
            if (!String.IsNullOrEmpty(paper.venue))
                return;
            if (String.IsNullOrEmpty(confvenue))
                Logger.Log($"Paper '{Walker.PureName(paper)}' lacks a venue, buts is parent conference lacks it too!");
            else
            {
                Paper f(Paper p)
                {
                    p.venue = confvenue;
                    return p;
                }
                Xformation action = new XPaper(f);
                Manager.RegisterAction("Paper lacks a venue", paper, action);
                //Logger.Log($"Paper '{Walker.PureName(paper)}' lacks a venue: TODO add an action!");
            }
        }
    }
}
