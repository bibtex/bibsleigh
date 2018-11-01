using System.Diagnostics;
using System.Windows;
using System.Windows.Controls;
using XFit.refine;
using XFit.ast;

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
