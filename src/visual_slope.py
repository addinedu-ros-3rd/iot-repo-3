from serial import Serial, serialutil
import time
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.lines import Line2D
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
from PyQt5.QtCore import Qt, QTimer
import time
import pyqtgraph as pg
from pyqtgraph import PlotWidget, plot
import math
from_class = uic.loadUiType("visual_slope.ui")[0]
class WindowClass(QMainWindow, from_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.graphWidget.setXRange(-200, 200)
        self.graphWidget.setYRange(0, 200)
        self.x = [0, 0]
        self.y = [0, 0]
        try :
            self.serial_port = Serial(port="/dev/ttyACM1",
            baudrate=9600)
            time.sleep(2)
            self.timer = QTimer()
            self.timer.timeout.connect(self.update_line)
            self.timer.start(100)  # Update every 100 ms
        except serialutil.SerialException as se:
            print(f'SerialException: {se}')
        except FileNotFoundError as fnfe:
            print(f'FileNotFoundError: {fnfe}')
    def update_line(self):
        try:
            data = self.serial_port.readline().decode('utf-8').strip()
            angle_list = [float(val) for val in data.split('|')]
            print(f'{angle_list[1]}')
            print(f'{angle_list}\n')
            self.labelAngle.setText(str(angle_list[1]))
            self.graphWidget.clear()
            angle_rad = math.radians(int(angle_list[1]))
            #해당 1사분면과 2사분면을 왔다갔다 하는 함수
            line_x = 200 * math.cos(angle_rad)
            line_y = 200 * math.sin(angle_rad)
            self.x[-1] = line_x
            self.y[-1] = line_y
            self.graphWidget.plot(self.x, self.y, pen = 'r')
        except ValueError as ve:
            print(f'ValueError : {ve}')
        except Exception as e:
            print(f'an error occurred : {e}')
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWindows = WindowClass()
    myWindows.show()
    sys.exit(app.exec_())
