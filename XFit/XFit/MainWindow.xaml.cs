using System.Windows;
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
            Logger._log = Log;
        }

        private void Read_Click(object sender, RoutedEventArgs e)
        {
            _main = new Sleigh(Path.Text);
            Logger.Log($"Read {_main.NoOfDomains} domains");
        }

        private void Write_Click(object sender, RoutedEventArgs e)
        {
        }

        private void Quit_Click(object sender, RoutedEventArgs e)
            => this.Close();
    }
}
