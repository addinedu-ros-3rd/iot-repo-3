# UI용 모듈
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
import urllib.request
# matplot용 모듈
import serial
import matplotlib.pyplot as plt
from collections import deque

# 아두이노 시리얼 통신 설정
ser = serial.Serial(
    port='/dev/ttyACM2',
    baudrate=9600
)

# 서브플롯 설정
num_sensors = 5  # 센서 개수
fig, axs = plt.subplots(num_sensors, 1, sharex=True, figsize=(6, 10))

# 서브플롯별 데이터 초기화
sensor_data = [[] for _ in range(num_sensors)]

for ax in axs:
    ax.set_xlim(0, 10)  # 초기 x 범위 설정
    ax.set_ylim(0, 100)  # y 범위 설정

# 시간 데이터 초기화
x = deque(maxlen=10)
timing = 0

while True:
    data = ser.readline().decode('utf-8').strip()  # 시리얼 데이터를 읽고 디코드합니다.
    sensor_values = [float(val) for val in data.split('|')]  # 읽은 데이터를 부동 소수점으로 변환
    
    x.append(timing)  # x 데이터에 시간 값을 추가
    timing += 1
    
    for i in range(num_sensors):
        sensor_data[i].append(sensor_values[i])  # 각 센서 값 데이터 추가
    
    # 서브플롯 업데이트
    for i in range(num_sensors):
        axs[i].clear()  # 서브플롯을 지우고 다시 그립니다.
        axs[i].plot(x, sensor_data[i], marker='o')  # 서브플롯에 그래프를 그립니다.
        axs[i].set_xlabel('Time')
        axs[i].set_ylabel(f'Sensor {i+1} Value')
        axs[i].set_title(f'Real-time Sensor {i+1} Data')
    
    plt.pause(1)  # 1초마다 그래프를 업데이트
# # 그래프 초기화
# plt.ion()
# fig, axs = plt.subplots(5, 1, sharex=True)  # sharex로 x축을 공유.

# for ax in axs:
#     ax.set_xlim(0, 20)  # 초기 x 범위 설정
#     ax.set_ylim(-500, 500)  # y 범위 설정

# t = deque(maxlen=10)
# Deg_X = deque(maxlen=10)
# Deg_Y = deque(maxlen=10)
# Deg_Z = deque(maxlen=10)
# servoL = deque(maxlen=10)
# servoR = deque(maxlen=10)

# # 시간은 0초부터
# timing = 0

# # 시리얼 읽어오기
# while True:
#     if ser.readable():
#         sentence = ser.readline().decode().strip()  # 시리얼을 한 줄 가져옴
#         values_list = [int(value) for value in sentence.split('|')]  # |을 기준으로 split한 다음 values_list에 리스트형으로 변환.

#         # 데크에 값을 추가.
#         t.append(timing); timing += 1  # t값을 계속 추가.
#         Deg_X.append(values_list[0])
#         Deg_Y.append(values_list[1])
#         Deg_Z.append(values_list[2])
#         servoL.append(values_list[3])
#         servoR.append(values_list[4])
        
#         print(f'{t}, {values_list[0]}, {values_list[1]}, {values_list[2]}, {values_list[3]}, {values_list[4]}')  # 센서값 출력위한 라인.
        
#         # 서브플롯 업데이트
#         axs[0].clear()  # 서브플롯을 지우고 다시 그리기.
#         axs[0].plot(t, values_list[0], marker='o')
#         axs[0].set_xlabel('Time')
#         axs[0].set_ylabel('Deg_X')        

#         plt.pause(1)
                     


# 그래프 초기화 및 Line2D 객체 생성
# plt.ion()
# fig, axs = plt.subplots(1, 7, sharex=True, figsize=(12, 6), facecolor='lightgray')
# lines = [Line2D([], []) for _ in range(7)]
# lines = [Line2D([], []) for _ in range(5)]

# for i, ax in enumerate(axs):
#     ax.set_ylim(y_ranges[list(y_ranges.keys())[i]][0], y_ranges[list(y_ranges.keys())[i]][1])
#     ax.grid()
#     ax.set_xlabel("Time")
#     ax.set_ylabel("Value")
#     ax.set_title(list(y_ranges.keys())[i])
#     ax.add_line(lines[i])  # Line2D 객체 추가

# x = 0


# # 함수 해당 값 실시간 수정
# def chart_update(x_values, Deg_X, Deg_Y, Deg_Z, servoL, servoR):
#     for i, line in enumerate(lines):
#         line.set_data(x_values, [Deg_X, Deg_Y, Deg_Z, servoL, servoR][i])
#         axs[i].relim()
#         axs[i].autoscale_view()

#     fig.canvas.draw()
#     fig.canvas.flush_events()


        # if len(data) == 7:
        #     dx = int(data[0])
        #     dy = int(data[1])
        #     dz = int(data[2])
        #     sl = int(data[3])
        #     sr = int(data[4])
            
        #     print(f"{dx},{dy},{dz},{sl},{sr}\n")

        #     if len(x_values) > 50: # db 저장시 삭제 요망
        #         x_values.pop(0)
        #         Deg_X.pop(0)
        #         Deg_Y.pop(0)
        #         Deg_Z.pop(0)
        #         servoL.pop(0)
        #         servoR.pop(0)

        #     # 데이터 업데이트
        #     x_values.append(x)
        #     Deg_X.append(dx)
        #     Deg_Y.append(dy)
        #     Deg_Z.append(dz)
        #     servoL.append(sl)
        #     servoR.append(sr)

        #     chart_update(x_values, Deg_X, Deg_Y, Deg_Z, servoL, servoR)

        # time.sleep(0.5)
        # x += 1

# # UI 파트
# from_class = uic.loadUiType("../ui/final_project.ui")[0]
# class WindowClass(QMainWindow, from_class):
#     def __init__(self):
#         super().__init__()
#         self.setupUi(self)

# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     myWindows = WindowClass()
#     myWindows.show()

#     sys.exit(app.exec_())