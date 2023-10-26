import serial
import time
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D  # Line2D를 추가

ser = serial.Serial(
    port="/dev/ttyACM0",
    baudrate=9600,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
# 자이로 센서 데이터 리스트 초기화
aX_data, aY_data, aZ_data, tmp_data, gX_data, gY_data, gZ_data = [], [], [], [], [], [], []
x_values = []

# 그래프 범위 초기화 및 설정 
y_ranges = {
        "acX": (-5000, 5000),
        "acY": (-10000, 10000),
        "acZ": (-20000, 0),
        "Tmp": (0, 50),
        "gcX": (-200, 200),
        "gcY": (-200, 200),
        "gcZ": (-100, 50)
    }

# 그래프 초기화 및 Line2D 객체 생성
plt.ion()
fig, axs = plt.subplots(1, 7, sharex=True, figsize=(12, 6), facecolor='lightgray')
lines = [Line2D([], []) for _ in range(7)]

for i, ax in enumerate(axs):
    ax.set_ylim(y_ranges[list(y_ranges.keys())[i]][0], y_ranges[list(y_ranges.keys())[i]][1])
    ax.grid()
    ax.set_xlabel("Time")
    ax.set_ylabel("Value")
    ax.set_title(list(y_ranges.keys())[i])
    ax.add_line(lines[i])  # Line2D 객체 추가

x = 0

# 함수 해당 값 실시간 수정
def chart_update(x_values, aX_data, aY_data, aZ_data, tmp_data, gX_data, gY_data, gZ_data):
    for i, line in enumerate(lines):
        line.set_data(x_values, [aX_data, aY_data, aZ_data, tmp_data, gX_data, gY_data, gZ_data][i])
        axs[i].relim()
        axs[i].autoscale_view()

    fig.canvas.draw()
    fig.canvas.flush_events()

# 시리얼 통신으로 자이로 센서 값와서 표기
while True:
    if ser.readable():
        response = ser.readline()
        data = response.decode().strip().split(' | ')
        #data = response.split(b' | ')

        if len(data) == 7:
            aX = int(data[0])
            aY = int(data[1])
            aZ = int(data[2])
            tmp = float(data[3])
            gX = int(data[4])
            gY = int(data[5])
            gZ = int(data[6])

            print(f"{aX},{aY},{aZ},{tmp},{gX},{gY},{gZ}\n")

            if len(x_values) > 50: # db 저장시 삭제 요망
                x_values.pop(0)
                aX_data.pop(0)
                aY_data.pop(0)
                aZ_data.pop(0)
                tmp_data.pop(0)
                gX_data.pop(0)
                gY_data.pop(0)
                gZ_data.pop(0)

            # 데이터 업데이트
            x_values.append(x)
            aX_data.append(aX)
            aY_data.append(aY)
            aZ_data.append(aZ)
            tmp_data.append(tmp)
            gX_data.append(gX)
            gY_data.append(gY)
            gZ_data.append(gZ)

            chart_update(x_values, aX_data, aY_data, aZ_data, tmp_data, gX_data, gY_data, gZ_data)

        time.sleep(0.5)
        x += 1
