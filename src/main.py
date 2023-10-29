import time
from serial import Serial
import sys
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *
from PyQt6 import uic
import re
from datetime import datetime
import mysql.connector

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

table_name = "log_" + str(current_time)

sql_command1 = f"CREATE TABLE {table_name} (Deg_X int, Deg_Y int, Deg_Z int, Servo_L int, Servo_R int)"
sql_command2 = f"INSERT INTO {table_name} VALUES (%s, %s, %s, %s, %s)"
print(sql_command2)

cur = remote.cursor()
cur.execute(sql_command1)

# 시리얼 패턴
pattern = r"(\d+), (\d+)"

arduino_s = None  # 글로벌 변수 선언. s값을 저장하기 위한 용도
arduino_m = None  # 글로벌 변수 선언. s값을 저장하기 위한 용도
g_buffer = None  # 글로벌 변수 선언. 자동모드에서 동작 로그를 저장하기 위한 용도
tmp = 0  # 글로벌 변수 선언. 임시용

# UI 파트(메인 코드)
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

        self.timer = QTimer(self)  # timer 변수에 QTimer 할당
        self.timer.timeout.connect(self.status_report)  # start timeout 시에 연결할 함수. 즉, 1초마다 상태값을 가져오는 함수를 호출.
        self.timer.start(100)  # 1초마다 반복    

        self.btn_status.clicked.connect(self.btnStatus)  # 시작|정지 버튼
        self.btn_mode.clicked.connect(self.btnMode)      # 수동|자동 버튼
        
        self.str_angle = ""  # 수동모드 일 경우, 값을 저장할 변수

        self.n9.clicked.connect(self.btn_n9)             # 숫자 9 버튼 ~
        self.n8.clicked.connect(self.btn_n8)
        self.n7.clicked.connect(self.btn_n7)
        self.n6.clicked.connect(self.btn_n6)
        self.n5.clicked.connect(self.btn_n5)
        self.n4.clicked.connect(self.btn_n4)
        self.n3.clicked.connect(self.btn_n3)
        self.n2.clicked.connect(self.btn_n2)
        self.n1.clicked.connect(self.btn_n1)
        self.n0.clicked.connect(self.btn_n0)             # ~ 숫자 0 버튼
        self.btndel.clicked.connect(self.btn_del)        # 백스페이스 버튼
        self.btnset.clicked.connect(self.btn_set)           # 각도를 반영하는 버튼

    def btn_set(self):
        global arduino_m
        if arduino_m == 0:
            command = " " + self.str_angle + "\n"
            self.conn.write(command.encode())
            self.str_angle = ""
            self.lineEdit.setText(self.str_angle)

    def str_angle_check(self):
        if int(self.str_angle) > 181 or int(self.str_angle) < -1:  # 0과 180 사이가 아니면
            self.str_angle = ""  # 강제로 문자열 비우기
            self.lineEdit.setText(self.str_angle)

    def btn_del(self):
        if len(self.str_angle) > 0:
            self.str_angle = self.str_angle[:-1]
            self.lineEdit.setText(self.str_angle)

    def btn_n9(self):  # 9 입력
        self.str_angle += "9"
        self.lineEdit.setText(self.str_angle)
        self.str_angle_check()

    def btn_n8(self):  # 8 입력
        self.str_angle += "8"
        self.lineEdit.setText(self.str_angle)
        self.str_angle_check()

    def btn_n7(self):  # 7 입력
        self.str_angle += "7"
        self.lineEdit.setText(self.str_angle)
        self.str_angle_check()
    
    def btn_n6(self):  # 6 입력
        self.str_angle += "6"
        self.lineEdit.setText(self.str_angle)
        self.str_angle_check()

    def btn_n5(self):  # 5 입력
        self.str_angle += "5"
        self.lineEdit.setText(self.str_angle)
        self.str_angle_check()
    
    def btn_n4(self):  # 4 입력
        self.str_angle += "4"
        self.lineEdit.setText(self.str_angle)
        self.str_angle_check()
    
    def btn_n3(self):  # 3 입력
        self.str_angle += "3"
        self.lineEdit.setText(self.str_angle)
        self.str_angle_check()

    def btn_n2(self):  # 2 입력
        self.str_angle += "2"
        self.lineEdit.setText(self.str_angle)
        self.str_angle_check()

    def btn_n1(self):  # 1 입력
        self.str_angle += "1"
        self.lineEdit.setText(self.str_angle)
        self.str_angle_check()
    
    def btn_n0(self):  # 0 입력
        self.str_angle += "0"
        self.lineEdit.setText(self.str_angle)
        self.str_angle_check()

    def status_report(self):
        global arduino_s, arduino_m
        print(arduino_s, arduino_m)
            
        if arduino_s == 1:
            self.STATUS.setText("ON")
            self.btn_status.setText("정지")

            if arduino_m == 1:
                self.MODE.setText("AUTO")
                self.btn_mode.setText("수동")
                self.start_record()
            else:
                self.MODE.setText("MANUAL")
                self.btn_mode.setText("자동")

        else:
            self.STATUS.setText("OFF")
            self.btn_status.setText("시작")
            self.MODE.setText("")

    def start_record(self):
        global sql_command2, remote, g_buffer
        try:
            nums = tuple(map(int, g_buffer.split(', ')))  # d버퍼 값들을 튜플로 받아서 sql insert.
            cursor = remote.cursor(buffered=True)
            print(nums)
            cursor.execute(sql_command2, (str(nums[0]), str(nums[1]), str(nums[2]), str(nums[3]), str(nums[4])))
            remote.commit()
        except Exception as e:
            print("Wrong Signal")

    def btnStatus(self):
        command = "s"
        self.conn.write(command.encode())
    
    def btnMode(self):
        command = "m"
        self.conn.write(command.encode())

class SerialManager(QThread):
    receive = pyqtSignal(str)

    def __init__(self, serial=None):
        super().__init__()
        self.serial = serial
        self.running = True

    def run(self):
        global arduino_s, arduino_m, g_buffer, tmp
        while self.running == True:
            try:
                if self.serial.readable():
                    res = self.serial.readline().decode('utf-8').strip()
                    
                    if re.match(pattern, res):  # 패턴 1에 해당하는 데이터인지 확인
                        arduino_s, arduino_m = map(int, res.split(', '))
                    else:
                        g_buffer = res

            except:
                print('Waiting...')

if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()

    sys.exit(app.exec())