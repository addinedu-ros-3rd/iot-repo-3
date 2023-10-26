# UI용 모듈
# import sys
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# from PyQt5 import uic
# import urllib.request
# matplot용 모듈
import serial
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from queue import Queue
# DB용 코드
import mysql.connector
from datetime import datetime

# DB에 접근
remote = mysql.connector.connect(
    host = "database-1.ciifx43v3wkq.ap-northeast-2.rds.amazonaws.com",
    port = 3306,
    user = "root",
    password = "qaz51133",
    database = "IOT" # 기존에 만든 IOT 데이터베이스를 USE
)

# 현재날짜, 시간 테이블을 생성.
current_time = datetime.now()  # 일단 날짜 시간을 가져옴.
current_time = current_time.strftime("%y_%m_%d_%H_%M_%S")  # 원하는 형식에 맞게 수정
sql_command = f"CREATE TABLE log_{current_time} (timing int, Deg_X int, Deg_Y int, Deg_Z int, Servo_L int, Servo_R int)"
cur = remote.cursor()
cur.execute(sql_command)

# # 아두이노 시리얼 통신 설정
ser = serial.Serial(
    port='/dev/ttyACM3',  # 연결할 때마다 바뀜
    baudrate=9600
)

# 서브플롯 설정
fig, axs = plt.subplots(5, 1, sharex=True, figsize=(6, 10))

# 각 y축의 출력 범위 고정
y_limits = [(-400, 400), (-400, 400), (-400, 400), (-200, 200), (-200, 200)]
for idx, ax in enumerate(axs):
    ax.set_ylim(y_limits[idx])

# 데이터 큐 초기화
timing = Queue(maxsize=10); [timing.put(0) for _ in range(10)]
degX = Queue(maxsize=10); [degX.put(0) for _ in range(10)]
degY = Queue(maxsize=10); [degY.put(0) for _ in range(10)]
degZ = Queue(maxsize=10); [degZ.put(0) for _ in range(10)]
servoL = Queue(maxsize=10); [servoL.put(0) for _ in range(10)]
servoR = Queue(maxsize=10); [servoR.put(0) for _ in range(10)]

# 시간 값 초기화
time_value = -1
remote.close()



def update(frame):
    # 전역변수를 사용하여 timing 갱신
    global time_value  
    time_value += 1
    
    data = ser.readline().decode().strip()  # 시리얼 데이터를 읽고 디코드.
    values = data.split('|')
    print(values)

    timing.get()  # timing 큐에 시간 get
    degX.get()  # DegX 큐에 값 get
    degY.get()  # DegY 큐에 값 get
    degZ.get()  # DegZ 큐에 값 get
    servoL.get()  # servoL 큐에 값 get
    servoR.get()  # servoR 큐에 값 get

    timing.put(time_value)  # timing 큐에 시간 put
    
    degX.put(values[0])  # DegX 큐에 값 put
    degY.put(values[1])  # DegY 큐에 값 put
    degZ.put(values[2])  # DegZ 큐에 값 put
    servoL.put(values[3])  # servoL 큐에 값 put
    servoR.put(values[4])  # servoR 큐에 값 put

    x_val = list(timing.queue)
    degX_y_val = list(degX.queue)
    degY_y_val = list(degY.queue)
    degZ_y_val = list(degZ.queue)
    servoL_y_val = list(servoL.queue)
    servoR_y_val = list(servoR.queue)
    line.set_data(x[:10], y[:10])
    return line,

ani = FuncAnimation(fig, update, blit=True)

plt.show()