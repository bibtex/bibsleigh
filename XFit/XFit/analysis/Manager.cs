using System.Collections.Generic;
using System.Linq;
using System.Windows.Controls;
using XFit.ast;

namespace XFit.analysis
{
    internal static class Manager
    {
        private static ListBox _recList;
        private static ListBox _fileList;
        private static TextBox _bef;
        private static TextBox _aft;
        private static int _recSelected = -1;
        private static string _rootPath;

        private static readonly IEnumerable<CorpusVisitor> checkers = new List<CorpusVisitor>()
        {
            new EmptyVenueFinder(),
        };

        internal static void InitialiseManager(ListBox top, ListBox left, TextBox before, TextBox after)
        {
            _recList = top;
            _fileList = left;
            _bef = before;
            _aft = after;
        }

        private static List<Recommender> recs = new List<Recommender>();

        internal static void FullAnalysis(Sleigh root)
        {
            _rootPath = root.FileName;
            foreach (var tool in checkers)
                root.Accept(tool);
        }

        internal static void RegisterAction(string title, Serialisable input, Xformation action)
        {
            Recommender rec = recs.FirstOrDefault(r => r.Name == title);
            if (rec == null)
            {
                rec = new Recommender(title);
                recs.Add(rec);
                _recList.Items.Add(rec.Name);
            }
            rec.Add(input, action);
        }

        internal static void HighlightRecommender(int index)
        {
            _fileList.Items.Clear();
            if (index < 0 || index >= recs.Count)
                return;
            _recSelected = index;
            foreach (var file in recs[index].Files)
                _fileList.Items.Add(file.Replace(_rootPath, ""));
        }

        internal static void HighlightFile(int index)
        {
            if (_recSelected < 0 || _recSelected >= recs.Count || index < 0 || index >= recs[_recSelected].Count)
            {
                _bef.Clear();
                _aft.Clear();
                return;
            }
            recs[_recSelected].HighlightFile(index, _bef, _aft);
        }

        internal static void DisposeFile(int index, bool run)
        {
            _bef.Clear();
            _aft.Clear();
            if (_recSelected < 0 || _recSelected >= recs.Count || index < 0 || index >= recs[_recSelected].Count)
                return;
            if (run)
                recs[_recSelected].RunForOne(index);
            Logger.Log($"The recommendation of '{recs[_recSelected].Name}' followed for '{_fileList.Items[index]}'.");
            _fileList.Items.RemoveAt(index);
            recs[_recSelected].RemoveFile(index);
        }

        internal static void RunCurrentRec()
        {
            _bef.Clear();
            _aft.Clear();
            var cx = _fileList.Items.Count;
            _fileList.Items.Clear();
            if (_recSelected < 0 || _recSelected >= recs.Count)
                return;
            recs[_recSelected].RunForAll();
            Logger.Log($"All {cx} recommendations of '{recs[_recSelected].Name}' followed.");
            _recList.Items.RemoveAt(_recSelected);
            recs.RemoveAt(_recSelected);
            _recSelected = -1;
        }
    }
}
