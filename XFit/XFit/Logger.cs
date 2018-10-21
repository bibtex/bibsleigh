using System.Windows.Controls;

namespace XFit
{
    internal static class Logger
    {
        internal static TextBox _log;

        internal static void Log(string msg)
        {
            _log.Text = msg + "\n" + _log.Text;
        }
    }
}
