# 통신 모듈
from serial import Serial

# UI 모듈
import time
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import uic

# DB 모듈
import mysql.connector
from datetime import datetime
import re

# 시리얼 패턴 정리
pattern1 = r"(\d+), (\d+)"
pattern2 = r"Deg_X: (\d+) \| Deg_Y: (\d+) \| Deg_Z: (\d+) \| ServoL: (\d+) \| ServoL: (\d+)"
# DB에 접근
remote = mysql.connector.connect(
    host = "database-1.ciifx43v3wkq.ap-northeast-2.rds.amazonaws.com",
    port = 3306,
    user = "root",
    password = "qaz51133",
    database = "IOT" # 기존에 만든 IOT 데이터베이스를 USE
)

# # DB에 현재날짜, 시간 테이블을 생성.
# current_time = datetime.now()  # 일단 날짜 시간을 가져옴.
# current_time = current_time.strftime("%y_%m_%d_%H_%M_%S")  # 원하는 형식에 맞게 수정
# sql_command = f"CREATE TABLE log_{current_time} (timing int, Deg_X int, Deg_Y int, Deg_Z int, Servo_L int, Servo_R int)"
# cur = remote.cursor()
# cur.execute(sql_command)

# remote.close()

# 메인 코드
from_class = uic.loadUiType("serial.ui")[0]

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Controller")

        self.conn = Serial(port='/dev/ttyACM0',
                           baudrate=9600)
        self.serial = SerialManager(self.conn)
        self.serial.start()

        self.pushButton.clicked.connect(self.Send)
        self.serial.receive.connect(self.Recv)
        
    def Send(self):
        text = self.lineEdit.text()
        text += "\n"
        self.conn.write(text.encode())

        #if self.conn.readable():
        #    res = self.conn.readline()
        #    self.textEdit.append(res.decode())

    def Recv(self, message):
        self.textEdit.append(message)


class SerialManager(QThread):
    receive = pyqtSignal(str)

    def __init__(self, serial=None):
        super().__init__()
        self.serial = serial
        self.running = True

    def run(self):
        while self.running == True:
            if self.serial.readable():
                res = self.serial.readline().decode()
                if len(res) > 0:
                    self.receive.emit(str(res))
            time.sleep(0.1)

    def stop(self):
        self.running = False


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()

    sys.exit(app.exec())