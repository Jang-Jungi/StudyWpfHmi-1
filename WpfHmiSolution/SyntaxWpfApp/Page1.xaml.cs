using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;
using BusinessLogic;

namespace SyntaxWpfApp
{
    /// <summary>
    /// Page1.xaml에 대한 상호 작용 논리
    /// </summary>
    public partial class Page1 : Page
    {
        public Page1()
        {
            InitializeComponent();

            InitCar();
        }

        private void InitCar()
        {
            var human = new Human();
            human.FirstName = "Lallies";
            human.HasLicense = false;

            Car car = new Car();
            car.Color = Colors.Red;
            car.Speed = 320.0;
            car.Driver = human;

            //car2.Color;

            //LblCarSpeed.Content = car.Speed;
        }

        private void BtnGo_Click(object sender, RoutedEventArgs e)
        {
            NavigationService.Navigate(new Uri("/Page2.xaml", UriKind.RelativeOrAbsolute));
        }
    }
}
