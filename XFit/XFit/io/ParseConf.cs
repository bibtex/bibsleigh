using XFit.ast;

namespace XFit.io
{
    public static partial class Parser
    {
        private static void ParseConf(string path, dynamic input, Conference output)
        {
            foreach (var file in Walker.EveryJSON(path))
            {
                if (Walker.FileExists(file))
                    output.AddPaper(file);
                else
                    Logger.Log($"File out of place: '{file}'");
            }

        }
    }
}
