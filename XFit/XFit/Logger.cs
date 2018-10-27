using System.Windows.Controls;

namespace XFit
{
    internal static class Logger
    {
        private static TextBox _log;

        internal static void InitialiseLogger(TextBox tb)
        {
            _log = tb;
        }

        internal static void Log(string msg)
        {
            _log.Text = msg + "\n" + _log.Text;
        }
    }
}
