using System;

namespace xbib
{
    class Program
    {
        static void Main(string[] args)
        {
            foreach(var arg in args)
            {
                var x = new XBibProcessor(arg);
                x.Engage();
            }
        }
    }
}
