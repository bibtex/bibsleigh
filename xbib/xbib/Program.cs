using System;

namespace xbib
{
    internal static class Config
    {
        internal static bool Debug { get; } = false;
    }

    internal class Program
    {
        private static void Main(string[] args)
        {
            Console.WriteLine("xbib 1.0.0.0");
            foreach (var arg in args)
            {
                var x = new XBibProcessor(arg);
                x.Engage();
            }
        }
    }
}