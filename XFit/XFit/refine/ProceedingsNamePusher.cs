using System;
using XFit.ast;
using XFit.io;

namespace XFit.refine
{
    internal class ProceedingsNamePusher : CorpusVisitor
    {
        private string conftitle;
        private string confshort;

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
            if (!String.IsNullOrEmpty(conference.title))
            {
                conftitle = conference.title;
                if (String.IsNullOrEmpty(conference.booktitle))
                {
                    confshort = conference.venue;
                    if (String.IsNullOrEmpty(confshort))
                        confshort = Walker.PureName(conference).Split('-')[0];
                }
                else
                    confshort = conference.booktitle;
                return true;
            }
            else
                return false;
        }

        public override void ExitConference(Conference conference)
        {
            conftitle = String.Empty;
            confshort = String.Empty;
        }

        public override void VisitPaper(Paper paper)
        {
            if (paper.booktitle == conftitle && paper.booktitleshort == confshort)
                return;
            if (!String.IsNullOrEmpty(paper.journal))
                return;
            if (paper.booktitle != confshort && paper.booktitle != conftitle && String.IsNullOrEmpty(paper.booktitle))
                Logger.Log($"Unexpected booktitle on a paper: '{paper.booktitle}' (instead of '{confshort}')");
            else
            {
                Xformation action = new XPaper(GenPaperAction(conftitle, confshort));
                Manager.RegisterAction("Align booktitle of a paper with the title of its conference", paper, action);
            }
        }

        private Func<Paper, Paper> GenPaperAction(string fullN, string shortN)
            => p =>
            {
                var p2 = Parser.Clone(p);
                p2.booktitle = fullN;
                p2.booktitleshort = shortN;
                return p2;
            };
    }
}
