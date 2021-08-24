using SyntaxWpfApp;
using System.Windows.Media;

namespace BusinessLogic
{
    public class Car : Notifier
    {
        private double speed;
        public double Speed {
            get { return speed; }
            set
            {
                speed = value;
                OnPropertyChanged("Speed"); // 값이 변경됨을 시스템에 알려줌
            } 
        }
        public Color Color { get; set; }
        public Human Driver { get; set; }
    }

    public class Human
    {
        public string FirstName { get; set; }
        public bool HasLicense { get; set; }
    }
}
