# QT Designer 연동 소스
from PyQt5 import QtGui, QtWidgets, uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import sys

import paho.mqtt.client as mqtt
import json
import datetime as dt
import RPi.GPIO as GPIO
import time
# 여기에 GPIO 작업 및 MQTT 송수신을 처리함

dev_id = "machine01"
broker_address = "192.168.200.102"
broker_port = 1883
client = None

redPin = 18
greenPin = 23
bluePin = 24

GPIO.setmode(GPIO.BCM) # BOARD or BCM
GPIO.setup(redPin, GPIO.OUT)
GPIO.setup(greenPin, GPIO.OUT)
GPIO.setup(bluePin, GPIO.OUT)

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
        GPIO.output(greenPin, True)
        GPIO.output(bluePin, False)
        GPIO.output(redPin, False)

        print('LED를 켰습니다!!')
        self.lblStatus.setText('LED를 켰습니다')
        global client
        client.publish("machine01/4001/", json.dumps({"test": "pushpush"}), 1)

    def btnWarn_Clicked(self):
        GPIO.output(greenPin, False)
        GPIO.output(bluePin, False)
        GPIO.output(redPin, True)

        print('경고상태.')
        self.lblStatus.setText('경고상태 입니다')
        global client
        client.publish("machine01/4001/", json.dumps({"test": "warnwarn"}), 1)


client = mqtt.Client(dev_id)
client.connect(broker_address, port=broker_port)
client.loop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MyWindow()
    sys.exit(app.exec_())