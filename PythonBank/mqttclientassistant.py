#coding: utf-8
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, uic
import paho.mqtt.client as mqtt
from datetime import datetime

import os
import sys

if getattr(sys, 'frozen', False):
    APP_DIR = sys._MEIPASS
else:
    APP_DIR = os.path.dirname(os.path.abspath(__file__))
uifile = os.path.join(APP_DIR, "mqttclient.ui")
ui_mainwindow, qtbaseclass = uic.loadUiType(uifile)


class MqttClientAssistant(ui_mainwindow, qtbaseclass):
    client = None
    is_connected = False
    topics = dict()  # TOPIC 목록

    def __init__(self, parent=None):
        if not parent:
            parent = self
        ui_mainwindow.__init__(parent)
        qtbaseclass.__init__(parent)
        self.setupUi(parent)
        self.setWindowTitle("MqttClientAssistant - MQTT클라이언트")

        self.client = mqtt.Client()
        self.client.on_connect = self.mqtt_on_connected
        self.client.on_message = self.mqtt_on_message
        # 서버 연결 없음, 구독 비활성화됨
        self.pushButton_sub.setEnabled(False)

    def slot_connect_pressed(self):
        # 서버 클릭 이벤트 연결
        if self.is_connected:  # 연결 및 처리 없이 종료
            return
        if self.lineEdit_server_port.text():
            port = int(self.lineEdit_server_port.text())
        else:
            port = 1883
        if self.lineEdit_user.text() and self.lineEdit_pwd.text():
            self.client.username_pw_set(self.lineEdit_user.text(),
                                        self.lineEdit_pwd.text())
        self.client.connect(self.lineEdit_server_ip.text(), port, 60)
        self.client.loop_start()

    def mqtt_on_connected(self, client, userdata, flags, rc):
        if rc == 0:
            print("Server Connected!")
            self.is_connected = True
            self.pushButton_sub.setEnabled(True)
            self.statusbar.showMessage("서버연결 성공!")
        else:
            self.statusbar.showMessage("서버연결 실패!")
            print("Server Connect Failed, with result code " + str(rc))

    def mqtt_on_message(self, client, userdata, msg):
        text = '[%s] %r:%s ' % (
            datetime.now().strftime('%Y-%m-%d %H:%M:%S,%f'), msg.topic,
            bytes.decode(msg.payload))
        print(text)
        self.textBrowser.append(text)

    def slot_sub_pressed(self):
        # 버튼 클릭 이벤트 구독
        if not self.is_connected:
            QMessageBox.critical(self, "오류", "서버연결 실패. 서버연결 우선!")
            return

        if self.topics:
            # topics = [(topic, qos) for topic, qos in self.topics.items()]
            topics = []
            text = ""
            for topic, qos in self.topics.items():
                text += "%r" % topic + "," + str(qos) + "\n"
                topics.append((topic, qos))
            self.client.subscribe(topics)
            self.lineEdit_topic.setToolTip("구독 TOPIC：\n" + text)

    def slot_topic_change(self):
        # 제목 텍스트 수정 이벤트(QOS 변경 이벤트도 이 기능에 바인딩됨)
        if self.lineEdit_topic.text() and self.lineEdit_qos.text():
            self.topics[self.lineEdit_topic.text()] = int(
                self.lineEdit_qos.text())

    def slot_msg_send(self):
        # 포스트 메시지 캐리지 리턴
        if not self.is_connected:
            QMessageBox.critical(self, "오류", "서버연결 실패. 서버연결 우선!")
            return

        topic = self.lineEdit_topic.text()
        msg = self.lineEdit_msg_pub.text()
        qos = self.lineEdit_qos.text()
        if topic and msg and qos:
            qos = int(qos)
            self.client.publish(topic, msg, qos)
            self.client.subscribe(topic, qos)