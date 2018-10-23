using Microsoft.VisualStudio.TestTools.UnitTesting;
using Newtonsoft.Json;
using System.IO;
using XFit.ast;
using XFit.io;

namespace BibTest
{
    [TestClass]
    public class UnitTest1
    {
        [TestMethod]
        public void TestPaper()
        {
            string path = @"C:\bigrepos\bibsleigh\json\corpus\SLE\2017\SLE-2017";
            JsonSerializerSettings settings = new JsonSerializerSettings
            {
                MissingMemberHandling = MissingMemberHandling.Error,
                NullValueHandling = NullValueHandling.Ignore
            };
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
            JsonSerializerSettings settings = new JsonSerializerSettings
            {
                MissingMemberHandling = MissingMemberHandling.Error,
                NullValueHandling = NullValueHandling.Ignore
            };
            foreach (var fname in Directory.GetFiles(path, "*.json", SearchOption.TopDirectoryOnly))
            {
                Parser.Unparse(
                    Parser.Parse<Domain>(fname),
                    fname + "_"
                    );
            }
        }
    }
}
