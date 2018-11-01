using Microsoft.VisualStudio.TestTools.UnitTesting;
using System.IO;
using XFit.analysis;
using XFit.ast;
using XFit.io;

namespace BibTest
{
    [TestClass]
    public class UnitTest1
    {
        [TestMethod]
        public void TestNamer1()
        {
            var pn = new ProceedingsNamer();
            var t1 = "16th Euromicro International Conference on Parallel, Distributed and Network-Based Processing (PDP 2008), 13-15 February 2008, Toulouse, France";
            var t2 = pn.Normalise(t1);
            Assert.AreEqual("Proceedings of the 16th Euromicro International Conference on Parallel, Distributed and Network-Based Processing", t2);
        }

        [TestMethod]
        public void TestNamer2()
        {
            var pn = new ProceedingsNamer();
            var t1 = "16th Euromicro International Conference on Parallel, Distributed and Network-Based Processing, PDP 2008, 13-15 February 2008, Toulouse, France";
            var t2 = pn.Normalise(t1);
            Assert.AreEqual("Proceedings of the 16th Euromicro International Conference on Parallel, Distributed and Network-Based Processing", t2);
        }

        //
        [TestMethod]
        public void TestNamer3()
        {
            var pn = new ProceedingsNamer();
            var t1 = "3rd Euromicro Workshop on Parallel and Distributed Processing (PDP '95), January 25-27, 1995, San Remo, Italy";
            var t2 = pn.Normalise(t1);
            Assert.AreEqual("Proceedings of the 3rd Euromicro Workshop on Parallel and Distributed Processing", t2);
        }

        [TestMethod]
        public void TestPaper()
        {
            string path = @"C:\bigrepos\bibsleigh\json\corpus\SLE\2017\SLE-2017";
            foreach (var fname in Directory.GetFiles(path, "*.json", SearchOption.TopDirectoryOnly))
            {
                Parser.Unparse(
                    Parser.Parse<Paper>(fname),
                    fname + "_"
                    );
            }
        }

        [TestMethod]
        public void TestDomain()
        {
            string path = @"C:\bigrepos\bibsleigh\json\corpus";
            foreach (var fname in Directory.GetFiles(path, "*.json", SearchOption.TopDirectoryOnly))
            {
                Parser.Unparse(
                    Parser.Parse<Domain>(fname),
                    fname + "_"
                    );
            }
        }

        [TestMethod]
        public void TestBrand()
        {
            string path = @"C:\bigrepos\bibsleigh\json\corpus\ARCH";
            foreach (var fname in Directory.GetFiles(path, "*.json", SearchOption.TopDirectoryOnly))
            {
                Parser.Unparse(
                    Parser.Parse<Brand>(fname),
                    fname + "_"
                    );
            }
        }

        [TestMethod]
        public void TestConf()
        {
            string path = @"C:\bigrepos\bibsleigh\json\corpus\SLE\2012";
            foreach (var fname in Directory.GetFiles(path, "*.json", SearchOption.TopDirectoryOnly))
            {
                Parser.Unparse(
                    Parser.Parse<Conference>(fname),
                    fname + "_"
                    );
            }
        }
    }
}
