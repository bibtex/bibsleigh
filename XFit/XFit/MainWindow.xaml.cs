using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using XFit.analysis;
using XFit.ast;
using XFit.refine;

namespace XFit
{
    /// <summary>
    /// Interaction logic for MainWindow.xaml
    /// </summary>
    public partial class MainWindow : Window
    {
        private Sleigh _main;

        public MainWindow()
        {
            InitializeComponent();
            Logger.InitialiseLogger(Log);
            Manager.InitialiseManager(RecsList, FileList, Before, After);
        }

        private void Read_Click(object sender, RoutedEventArgs e)
        {
            var S = new Stopwatch();
            S.Start();
            _main = new Sleigh(Path.Text);
            S.Stop();
            Logger.Log($"Read {_main.NoOfDomains} domains in {S.Elapsed}");
        }

        private void Analyse_Click(object sender, RoutedEventArgs e)
        {
            Manager.FullAnalysis(_main);
        }

        private void Calc_Click(object sender, RoutedEventArgs e)
        {
            Community c = new Community();
            _main.Accept(c);
            DumpData(c.AllAuthors, c.AuthorDict, "authors");
            DumpData(c.AllWords, c.VocabDict, "words");
            DumpData(c.AllTags, c.TagDict, "tags");
        }

        private void DumpData(SortedSet<string> keys, Dictionary<string, Dictionary<string, int>> dict, string file)
        {
            List<string> lines = new List<string>();
            lines.AddRange(keys);
            List<string> venues = dict.Keys.ToList();
            venues.Sort();
            foreach (string venue in venues)
            {
                int i = 0, num;
                foreach (var key in keys)
                {
                    if (dict[venue].ContainsKey(key))
                        num = dict[venue][key];
                    else
                        num = 0;
                    lines[i] += "," + num;
                    i++;
                }
            }
            File.WriteAllLines(System.IO.Path.Combine(Path.Text, file + ".csv"), lines);
        }

        private void Write_Click(object sender, RoutedEventArgs e)
        {
        }

        private void Quit_Click(object sender, RoutedEventArgs e)
            => this.Close();

        private void RecsList_SelectionChanged(object sender, System.Windows.Controls.SelectionChangedEventArgs e)
        {
            if (sender is ListBox box)
            {
                Manager.HighlightRecommender(box.SelectedIndex);
            }
        }

        private void FileList_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            if (sender is ListBox box)
            {
                Manager.HighlightFile(box.SelectedIndex);
            }
        }

        private void X_Click(object sender, RoutedEventArgs e)
        {
            Manager.DisposeFile(FileList.SelectedIndex, run: false);
        }

        private void Run_Click(object sender, RoutedEventArgs e)
        {
            Manager.DisposeFile(FileList.SelectedIndex, run: true);
        }

        private void RunAll_Click(object sender, RoutedEventArgs e)
        {
            Manager.RunCurrentRec();
        }
    }
}
