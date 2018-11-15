using System;
using XFit.ast;
using XFit.io;

namespace XFit.refine
{
    internal class StatusInferrer : CorpusVisitor
    {
        private const string ACTION_NAME = "Paper status made explicit";

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
            => true;

        public override void ExitConference(Conference conference)
        {
        }

        public override void VisitPaper(Paper paper)
        {
            if (String.IsNullOrEmpty(paper.title))
                return;
            if (!paper.title.EndsWith(")", StringComparison.InvariantCulture))
                return;
            int index = paper.title.LastIndexOf('(');
            // should never happen, but you never know
            if (index == 0 || paper.title[index - 1] != ' ')
                return;
            string main = paper.title.Substring(0, index).Trim();
            string brak = paper.title.Substring(index + 1);
            // get rid of the bracket
            brak = brak.Substring(0, brak.Length - 1).Trim();
            Xformation action;
            switch (brak.ToLower())
            {
                case "s": // happens in SEKE (probably corrupt metadata)
                case "full paper":
                    action = new XPaper(GenPaperAction(main));
                    Manager.RegisterAction(ACTION_NAME, paper, action);
                    break;
                case "abstract":
                case "abstract for talk":
                case "abstract only":
                case "talk abstract":
                case "detailed abstract":
                case "extended abstract":
                case "extended abstracts":
                case "extende abstract": // misspelling!
                case "extended summary":
                case "research summary":
                case "extended outline":
                case "summary":
                case "summaray": // misspelling!
                case "a summary":
                case "concise version":
                    action = new XPaper(GenPaperAction(main, "abstract"));
                    Manager.RegisterAction(ACTION_NAME, paper, action);
                    break;
                case "best paper":
                case "best paper award":
                case "awarded best paper!":
                    action = new XPaper(GenPaperAction(main, "best paper"));
                    Manager.RegisterAction(ACTION_NAME, paper, action);
                    break;
                case "an experience report":
                case "experience report":
                case "experience paper":
                case "status report":
                case "partial report":
                    action = new XPaper(GenPaperAction(main, "report"));
                    Manager.RegisterAction(ACTION_NAME, paper, action);
                    break;
                case "keynote":
                case "abstract of keynote address":
                case "keynote abstract":
                case "keynote address — abstract":
                case "keynote address":
                case "keynote paper":
                case "keynote talk":
                case "seip keynote": // special case
                    action = new XPaper(GenPaperAction(main, "keynote"));
                    Manager.RegisterAction(ACTION_NAME, paper, action);
                    break;
                case "industrial session":
                case "industrial paper":
                case "industrial talk":
                    action = new XPaper(GenPaperAction(main, "industrial"));
                    Manager.RegisterAction(ACTION_NAME, paper, action);
                    break;
                case "invited industrial talk":
                    action = new XPaper(GenPaperAction(main, "industrial", "invited"));
                    Manager.RegisterAction(ACTION_NAME, paper, action);
                    break;
                case "invited lecture":
                case "invited paper":
                case "invited presentation":
                case "invited talk":
                    action = new XPaper(GenPaperAction(main, "invited"));
                    Manager.RegisterAction(ACTION_NAME, paper, action);
                    break;
                case "abstract of invited tutorial":
                    action = new XPaper(GenPaperAction(main, "abstract", "invited", "tutorial"));
                    Manager.RegisterAction(ACTION_NAME, paper, action);
                    break;
                case "invited tutorial":
                    action = new XPaper(GenPaperAction(main, "invited", "tutorial"));
                    Manager.RegisterAction(ACTION_NAME, paper, action);
                    break;
                case "tutorial/keynote":
                    action = new XPaper(GenPaperAction(main, "keynote", "tutorial"));
                    Manager.RegisterAction(ACTION_NAME, paper, action);
                    break;
                case "invited talk abstract":
                case "invited talk, abstract only":
                case "abstract of an invited lecture":
                case "abstract of invited lecture":
                case "abstract of invited presentation":
                case "abstract of invited talk":
                case "extended abstract of invited talk":
                    action = new XPaper(GenPaperAction(main, "invited", "abstract"));
                    Manager.RegisterAction(ACTION_NAME, paper, action);
                    break;
                case "tutorial overview":
                case "tutorial abstract":
                case "abstract of a tutorial":
                case "extended abstract of a tutorial":
                    action = new XPaper(GenPaperAction(main, "tutorial", "abstract"));
                    Manager.RegisterAction(ACTION_NAME, paper, action);
                    break;
                case "short paper":
                case "short version":
                    action = new XPaper(GenPaperAction(main, "short"));
                    Manager.RegisterAction(ACTION_NAME, paper, action);
                    break;
                case "system descrition": // misspelling!
                case "system description":
                case "system descriptions":
                case "system exhibition":
                    action = new XPaper(GenPaperAction(main, "system description"));
                    Manager.RegisterAction(ACTION_NAME, paper, action);
                    break;
                case "tool":
                case "tool demo":
                case "tool demonstration":
                case "tool paper":
                case "tool presentation":
                    action = new XPaper(GenPaperAction(main, "tool"));
                    Manager.RegisterAction(ACTION_NAME, paper, action);
                    break;
                case "demo abstract":
                    action = new XPaper(GenPaperAction(main, "tool", "abstract"));
                    Manager.RegisterAction(ACTION_NAME, paper, action);
                    break;
                case "mini-tutorial":
                case "distilled tutorial":
                case "a tutorial":
                case "tutorial":
                case "tutorial session":
                    action = new XPaper(GenPaperAction(main, "tutorial"));
                    Manager.RegisterAction(ACTION_NAME, paper, action);
                    break;
                case "position statement":
                case "position paper":
                case "vision paper":
                    action = new XPaper(GenPaperAction(main, "vision"));
                    Manager.RegisterAction(ACTION_NAME, paper, action);
                    break;
                case "functional pearl":
                case "declarative pearl":
                    action = new XPaper(GenPaperAction(main, "pearl"));
                    Manager.RegisterAction(ACTION_NAME, paper, action);
                    break;
                case "a preliminary report":
                case "preliminary report":
                case "preliminary draft":
                case "preliminary version":
                case "work in progress":
                case "working paper":
                    action = new XPaper(GenPaperAction(main, "work in progress"));
                    Manager.RegisterAction(ACTION_NAME, paper, action);
                    break;
                case "preliminary abstract":
                case "preliminary extended abstract":
                    action = new XPaper(GenPaperAction(main, "abstract", "work in progress"));
                    Manager.RegisterAction(ACTION_NAME, paper, action);
                    break;
                case "system abstract":
                    action = new XPaper(GenPaperAction(main, "abstract", "system description"));
                    Manager.RegisterAction(ACTION_NAME, paper, action);
                    break;
                default:
                    Logger.Log($"Paper '{Walker.PureName(paper)}' has a strange potential status: '({brak})'");
                    break;
            }
        }

        private Func<Paper, Paper> GenPaperAction(string newtitle)
            => p =>
            {
                var p2 = Parser.Clone(p);
                p2.title = newtitle;
                return p2;
            };

        private Func<Paper, Paper> GenPaperAction(string newtitle, string status)
            => p =>
            {
                var p2 = Parser.Clone(p);
                p2.title = newtitle;
                p2.AddStatus(status);
                return p2;
            };

        private Func<Paper, Paper> GenPaperAction(string newtitle, string status1, string status2)
            => p =>
            {
                var p2 = Parser.Clone(p);
                p2.title = newtitle;
                p2.AddStatus(status1);
                p2.AddStatus(status2);
                return p2;
            };

        private Func<Paper, Paper> GenPaperAction(string newtitle, string status1, string status2, string status3)
            => p =>
            {
                var p2 = Parser.Clone(p);
                p2.title = newtitle;
                p2.AddStatus(status1);
                p2.AddStatus(status2);
                p2.AddStatus(status3);
                return p2;
            };
    }
}
