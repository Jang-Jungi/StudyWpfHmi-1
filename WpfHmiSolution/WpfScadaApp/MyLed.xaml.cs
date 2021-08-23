using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;

namespace WpfScadaApp
{
    /// <summary>
    /// MyLed.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class MyLed : UserControl
    {
        public MyLed()
        {
            InitializeComponent();
        }

        // 의존성 프로퍼티
        public static readonly DependencyProperty CurrStateProperty =
            DependencyProperty.Register("CurrState", typeof(Color), typeof(MyLed), new PropertyMetadata(Color.FromRgb(83, 86, 90)));

        public Color CurrState
        {
            get { return (Color)GetValue(CurrStateProperty);  }
            set { SetValue(CurrStateProperty, value); }
        }
    }
}
