# QT Designer 연동 소스
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys
# 여기에 GPIO 작업 및 MQTT 송수신을 처리함

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('./hmi_form.ui', self)

        #ui에 있는 위젯하고 시그널 처리(컨트롤 이벤트처리)
        self.btnOn.clicked.connect(self.btnOn_Clicked)
        self.btnWarn.clicked.connect(self.btnWarn_Clicked)
        self.lblStatus.setText('')

        self.initUI()

    def initUI(self):
        self.setWindowTitle('TEST HMI App')
        self.resize(1000, 600)
        self.center()
        self.showMaximized()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def btnOn_Clicked(self):
        print('LED를 켰습니다!!')
        self.lblStatus.setText('LED를 켰습니다')

    def btnWarn_Clicked(self):
        print('경고상태.')
        self.lblStatus.setText('경고상태 입니다')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyWindow()
    sys.exit(app.exec_())