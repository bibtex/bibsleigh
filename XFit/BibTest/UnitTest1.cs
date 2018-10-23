using Microsoft.VisualStudio.TestTools.UnitTesting;
using Newtonsoft.Json;
using System.IO;
using XFit.ast;

namespace BibTest
{
    [TestClass]
    public class UnitTest1
    {
        [TestMethod]
        public void TestMethod1()
        {
            string path = @"C:\bigrepos\bibsleigh\json\corpus\SLE\2017\SLE-2017";
            foreach (var fname in Directory.GetFiles(path, "*.json", SearchOption.TopDirectoryOnly))
            {
                string contents = File.ReadAllText(fname);
                Paper thing = JsonConvert.DeserializeObject<Paper>(contents);
                string result = JsonConvert.SerializeObject(thing, Formatting.Indented).Replace("  ", "\t");
                File.WriteAllText(fname + "_", result);
            }
        }
    }
}
