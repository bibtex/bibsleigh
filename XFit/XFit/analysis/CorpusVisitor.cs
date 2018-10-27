using XFit.ast;

namespace XFit.analysis
{
    public abstract class CorpusVisitor
    {
        public abstract void VisitSleigh(Sleigh sleigh);

        public abstract void VisitDomain(Domain domain);

        public abstract void VisitBrand(Brand brand);

        public abstract void VisitYear(Year year);

        public abstract void VisitConference(Conference conference);

        public abstract void VisitPaper(Paper paper);
    }
}
