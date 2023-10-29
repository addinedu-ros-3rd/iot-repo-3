# 시리얼 통신 모듈
import serial
# UI용 모듈
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import urllib.request
# matplot용 모듈
# import matplotlib.pyplot as plt
# from matplotlib.animation import FuncAnimation
# from queue import Queue
# DB용 코드
import mysql.connector
from datetime import datetime
import re

# DB에 접근
remote = mysql.connector.connect(
    host = "database-1.ciifx43v3wkq.ap-northeast-2.rds.amazonaws.com",
    port = 3306,
    user = "root",
    password = "qaz51133",
    database = "IOT" # 기존에 만든 IOT 데이터베이스를 USE
)

# DB에 현재날짜, 시간 테이블을 생성.
current_time = datetime.now()  # 일단 날짜 시간을 가져옴.
current_time = current_time.strftime("%y_%m_%d_%H_%M_%S")  # 원하는 형식에 맞게 수정
sql_command = f"CREATE TABLE log_{current_time} (timing int, Deg_X int, Deg_Y int, Deg_Z int, Servo_L int, Servo_R int)"
cur = remote.cursor()
cur.execute(sql_command)

remote.close()

# 아두이노 시리얼 통신 설정
ser = serial.Serial(
    port='/dev/ttyACM0',  # 연결할 때마다 바뀜
    baudrate=9600
)

# 시리얼 패턴 정리
pattern1 = r"(\d+), (\d+)"
pattern2 = r"Deg_X: (\d+) \| Deg_Y: (\d+) \| Deg_Z: (\d+) \| ServoL: (\d+) \| ServoL: (\d+)"

# UI 코드
from_class = uic.loadUiType("Giro.ui")[0]

class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("Controller")

        self.btn_status.clicked.connect(self.btnStatus)
        self.stauts_s = 0
        self.btn_mode.clicked.connect(self.btnMode)
        self.status_m = 0

        self.n9.clicked.connect(self.btn_n9)
        self.n8.clicked.connect(self.btn_n8)
        self.n7.clicked.connect(self.btn_n7)
        self.n4.clicked.connect(self.btn_n6)
        self.n5.clicked.connect(self.btn_n5)
        self.n4.clicked.connect(self.btn_n4)
        self.n3.clicked.connect(self.btn_n3)
        self.n2.clicked.connect(self.btn_n2)
        self.n1.clicked.connect(self.btn_n1)
        self.n0.clicked.connect(self.btn_n0)
        self.btndel.clicked.connect(self.btn_del)
        self.btnset.clicked.connect(self.btn_set)

        self.result = ""

        self.slider.valueChanged.connect(self.changeSilder)
    
    def changeSilder(self):
        if self.status_m == 0:
            the_val = " " + str(self.slider.value())
            ser.write(the_val.encode('utf-8'))
    
    def btn_set(self):
        if self.status_m == 0:
            the_val = " " + self.result
            print(self.result)
            ser.write(the_val.encode('utf-8'))
            self.result = ""

    def btn_del(self):
        if len(self.result) > 0:
            self.result = self.result[:-1]
            self.deg_visual.setText(self.result)

    def len_check(self):
        if len(self.result) > 3:
            self.result = self.result[:-1]
            self.deg_visual.setText(self.result)
    
    def btn_n9(self):  # 9
        self.result += "9"
        self.deg_visual.setText(self.result)
        self.len_check()
        
    def btn_n8(self):  # 8
        self.result += "8"
        self.deg_visual.setText(self.result)
        self.len_check()

    def btn_n7(self):  # 7
        self.result += "7"
        self.deg_visual.setText(self.result)
        self.len_check()

    def btn_n6(self):  # 6
        self.result += "6"
        self.deg_visual.setText(self.result)
        self.len_check()

    def btn_n5(self):  # 5
        self.result += "5"
        self.deg_visual.setText(self.result)
        self.len_check()

    def btn_n4(self):  # 4
        self.result += "4"
        self.deg_visual.setText(self.result)
        self.len_check()

    def btn_n3(self):  # 3
        self.result += "3"
        self.deg_visual.setText(self.result)
        self.len_check()

    def btn_n2(self):  # 2
        self.result += "2"
        self.deg_visual.setText(self.result)
        self.len_check()

    def btn_n1(self):  # 1
        self.result += "1"
        self.deg_visual.setText(self.result)
        self.len_check()

    def btn_n0(self):  # 0
        self.result += "0"
        self.deg_visual.setText(self.result)
        self.len_check()

    def btnStatus(self):  # 시작/정지 버튼을 누르면...
        ser.write(b's')
        self.stauts_s = not self.stauts_s

        if self.stauts_s == 1:
            self.STATUS.setText("ON")
            self.btn_status.setText("정지")
            
            self.status_m = 0
            self.MODE.setText("MANUAL")

        else:    
            self.STATUS.setText("OFF")
            self.MODE.setText("")
            self.btn_status.setText("시작")
        
    def btnMode(self):  # 모드 설정 버튼을 누르면...
        ser.write(b'm')
        self.status_m = not self.status_m

        if self.status_m == 1:
            self.MODE.setText("AUTO")
            self.btn_mode.setText("수동")
        else:
            self.MODE.setText("MANUAL")
            self.btn_mode.setText("자동")

# UI관련 코드
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()

    sys.exit(app.exec_())