using XFit.ast;

namespace XFit.refine
{
    public abstract class CorpusVisitor
    {
        public abstract bool EnterSleigh(Sleigh sleigh);

        public abstract void ExitSleigh(Sleigh sleigh);

        public abstract bool EnterDomain(Domain domain);

        public abstract void ExitDomain(Domain domain);

        public abstract void VisitBrand(Brand brand);

        public abstract bool EnterYear(Year year);

        public abstract void ExitYear(Year year);

        public abstract bool EnterConference(Conference conference);

        public abstract void ExitConference(Conference conference);

        public abstract void VisitPaper(Paper paper);
    }
}
