using System.Diagnostics;
using System.Windows;
using XFit.ast;
using XFit.io;

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
            Logger._log = Log;
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
            Logger.Log($"No analyses implemented yet!");
        }

        private void Write_Click(object sender, RoutedEventArgs e)
        {
        }

        private void Quit_Click(object sender, RoutedEventArgs e)
            => this.Close();
    }
}
