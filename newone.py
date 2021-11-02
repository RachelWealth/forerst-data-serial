# 实时数据显示预警程序
# -*- coding: utf-8 -*-
import threading
from datetime import datetime

import matplotlib
import matplotlib.pyplot as plt
import serial
from PyQt5.QtCore import QTimer, pyqtSlot
from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

from WriteIntoSQL import WriteIntoSQL

matplotlib.use("Qt5Agg")
from Real_time import Ui_MainWindow
import sys
import time
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
import dialog
from Myport import My_port
import serial.tools.list_ports
from neuralNetwork import BPNeuralNetwork

now = datetime.now()

global outTimeNum, lastState, modeChoice
outTimeNum = 0
modeChoice = 1
lastState = 1

# warning Dialog
MESSAGE = "DANGER!TOO MANY NUMBER OUTNUMBER THE CRITICAL NUMBER!"
TITLE = "MESSAGE"
HEAD = " time\t\tnumber\ttemperature（℃）\thumidity（rh）\tconcentration（ml/立方米）\tlight（lx）\tstate\n"
SQL_Table_name = 'time' + now.strftime("%Y%m%d")
global j_1, warningTimes
warningTimes = 1
j_1 = len(HEAD)

NumberOfGroups = ['2', '3', '4', '5', '6', '7', '8']  # 要统计的数据数量
baudrate_comboBox = ['100', '300', '600', '1200', '2400', '4800', '9600', '14400', '19200', '38400', '56000', '57600',
                     '115200', '128000', '256000']


class MyplotOne(FigureCanvas):
    def __init__(self, co="red", name="data", parent=None, width=10, height=6, dpi=100):
        # normalized for 中文显示和负号
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        # new figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        # 分区
        self.axes1 = self.fig.add_subplot(231)
        self.axes2 = self.fig.add_subplot(232)
        self.axes3 = self.fig.add_subplot(233)
        self.axes4 = self.fig.add_subplot(234)
        self.axes5 = self.fig.add_subplot(235)

        self.compute_initial_figure()

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


# class Myplot for plotting with matplotlib
class MyplotTwo(FigureCanvas):
    def __init__(self, co="red", name="data", parent=None, width=5, height=3, dpi=100):
        # normalized for 中文显示和负号
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        # new figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        # 分区
        self.axes = self.fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


# class dynamic_Graph for dynamic graph
class DynamicFigOne(MyplotOne):
    def __init__(self, *args, **kwargs):
        MyplotOne.__init__(self, *args, **kwargs)

    def compute_initial_figure(self):
        # input data
        # timex = [1,10]
        # temp1 = [0, 0]
        #
        # self.axes1.plot(timex, temp1, '-ob', color='blue', label='temperature')
        # self.axes2.plot(timex, temp1, '-ob', color='red', label='humidity')
        # self.axes3.plot(timex, temp1, '-ob', color='green', label='MQ2')
        # self.axes4.plot(timex, temp1, '-ob', color='black', label='MQ4')
        # self.axes5.plot(timex, temp1, '-ob', color='orange', label='light')

        ####################################################################################
        timex = range(1,11)
        temp1 = [26, 26, 25, 26, 27, 24, 25, 24, 26, 21]
        temp2 = [65, 56, 55, 66, 57, 64, 65, 64, 66, 63]
        temp3 = [18, 59, 55, 536, 857, 864, 505, 65, 85, 60]
        temp4 = [26, 56, 58, 56,68, 705, 562, 84, 66, 63]
        temp5 = [1025, 1046, 1052, 960, 652, 785, 890, 960, 1052, 1026]
        self.axes1.plot(timex, temp1, '-ob', color='blue', label='temperature')
        self.axes2.plot(timex, temp2, '-ob', color='red', label='humidity')
        self.axes3.plot(timex, temp3, '-ob', color='green', label='MQ2')
        self.axes4.plot(timex, temp4, '-ob', color='black', label='MQ4')
        self.axes5.plot(timex, temp5, '-ob', color='orange', label='light')



###################################################################################

        self.axes1.set_xlabel("time", fontsize=15)
        self.axes1.set_ylabel("temperature", fontsize=15)
        self.axes1.legend(loc=0, ncol=1)

        self.axes2.set_xlabel("time", fontsize=15)
        self.axes2.set_ylabel("humidity", fontsize=15)
        self.axes2.legend(loc=0, ncol=1)

        self.axes3.set_xlabel("time", fontsize=15)
        self.axes3.set_ylabel("MQ2", fontsize=15)
        self.axes3.legend(loc=0, ncol=1)

        self.axes4.set_xlabel("time", fontsize=15)
        self.axes4.set_ylabel("MQ4", fontsize=15)
        self.axes4.legend(loc=0, ncol=1)

        self.axes5.set_xlabel("time", fontsize=15)
        self.axes5.set_ylabel("light", fontsize=15)
        self.axes5.legend(loc=0, ncol=1)

        self.fig.tight_layout(pad=1, w_pad=0.1, h_pad=0)


# # 图标
# myLabels = ['temperature', 'humidity', 'concentrate', 'light']


class DynamicFigTwo(MyplotTwo):
    def __init__(self, *args, **kwargs):
        MyplotTwo.__init__(self, *args, **kwargs)

    def compute_initial_figure(self):
        # input data
        timex = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temp1 = [0, -1, -2, -1, 0, -3, -1, -1, -3, 0]
        temp2 = [45, 46, 45, 46, 44, 46, 44, 45, 46, 44]
        temp3 = [28, 30, 35, 28, 31, 32, 31, 35, 28, 32]
        temp4 = [36, 50, 43, 39, 42, 32, 31, 45, 28, 48]
        temp5 = [997, 996, 995, 997, 995, 167, 168, 175, 180, 167]
        self.axes.plot(timex, temp1, '-ob', color="blue", label="temperature")
        self.axes.plot(timex, temp2, '-ob', color="red", label="humidity")
        self.axes.plot(timex, temp3, '-ob', color="green", label="MQ2")
        self.axes.plot(timex, temp4, '-ob', color="black", label="MQ4")
        self.axes.plot(timex, temp5, '-ob', color="orange", label="light")
        self.axes.set_xlabel("time", fontsize=15)
        self.axes.set_ylabel("data", fontsize=15)
        self.axes.legend(loc=0, ncol=1)
        self.fig.tight_layout(pad=1, w_pad=0.1, h_pad=0)


"""
warningDialog defined myself
"""


# noinspection PyAttributeOutsideInit
class WarningQDialog(QMessageBox):
    def __init__(self, message):
        super(WarningQDialog, self).__init__()
        self.message = message
        self.initUI()

    def initUI(self):
        self.warningDialog = QMessageBox.warning(self, 'ERROR', self.message, QMessageBox.Abort)


# noinspection PyArgumentList
class ModeOneWindow(QMainWindow):
    def __init__(self, gridlayout):
        super(ModeOneWindow, self).__init__(parent=None)
        self.gridlayout = gridlayout
        self.fig = DynamicFigOne(dpi=120)
        self.fig_ntb = NavigationToolbar(self.fig, self)
        self.gridlayout.addWidget(self.fig, 0, 0, 1, 1)
        self.gridlayout.addWidget(self.fig_ntb, 1, 0, 1, 1)


class ModeTwoWindow(QMainWindow):
    def __init__(self, gridlayout, parent=None):
        super(ModeTwoWindow, self).__init__(parent)
        self.gridlayout = gridlayout
        self.fig = DynamicFigTwo(dpi=120)
        self.fig_ntb = NavigationToolbar(self.fig, self)
        self.gridlayout.addWidget(self.fig, 0, 0, 1, 1)
        self.gridlayout.addWidget(self.fig_ntb, 1, 0, 1, 1)


# noinspection PyProtectedMember,PyAttributeOutsideInit,PyBroadException,PyUnresolvedReferences,PyShadowingNames,PyGlobalUndefined
class AppWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(AppWindow, self).__init__(parent)
        global trainingSet
        # creating nuetral network with 5 input nodes, 3 hiden nodes and 1 output node
        self.neuralNetwork = BPNeuralNetwork()
        # testing neutral network
        self.neuralNetwork.test()

        self.setupUi(self)

        self.gridlayout = QGridLayout(self.Real_time_graph)
        self.ModeOneClicked()
        self.port_list.addItems(self.get_port_list())
        self.NumberComboBox.addItems(NumberOfGroups)
        self.Baudrate_comboBox.addItems(baudrate_comboBox)

        self._timer = QTimer(self)
        self._t = 1
        self.temperature = []
        self.humidity = []
        self.third = []
        self.forth = []
        self.fifth = []
        self.pass_time = []
        self.infor = ''
        self._Static_on = 0
        self._update_on = 0
        self.name = ''
        self.allowed_times = 0
        self.baudrate = 0
        self.critical = 0
        self.datas = []
        self.beginOrEnd = 1
        self.currentTime = ''
        self.SQL_helper = WriteIntoSQL(SQL_Table_name)
        self.state = 0

        # temp1 = [26, 26, 25, 26, 27, 24, 25, 24, 26, 21]
        # temp2 = [65, 56, 55, 66, 57, 64, 65, 64, 66, 63]
        # temp3 = [18, 59, 55, 536, 857, 864, 505, 65, 85, 60]
        # temp4 = [26, 56, 58, 56, 68, 705, 562, 84, 66, 63]
        # temp5 = [1025, 1046, 1052, 960, 652, 785, 890, 960, 1052, 1026]

        a = " time\t\t\ttemperature（℃）\t\t\thumidity（rh）\tMQ2（ml/立方米）\tMQ4（ml/立方米）\t\tlight（lx）\tstate\n"
        a = a + "01/10/21 16:05:26\t\t\t21\t\t\t63\t\t60\t\t\t\t63\t\t\t1026\t\tsafe\n"
        a = a + "01/10/21 16:05:24\t\t\t26\t\t\t66\t\t85\t\t\t\t66\t\t\t1052\t\tsafe\n"
        a = a + "01/10/21 16:05:22\t\t\t24\t\t\t64\t\t65\t\t\t\t66\t\t\t960\t\tsafe\n"
        a = a + "01/10/21 16:05:20\t\t\t25\t\t\t65\t\t505\t\t\t\t562\t\t\t890\t\tsafe\n"
        a = a + "01/10/21 16:05:18\t\t\t24\t\t\t64\t\t864\t\t\t\t705\t\t\t785\t\tsafe\n"
        a = a + "01/10/21 16:05:16\t\t\t27\t\t\t57\t\t857\t\t\t\t68\t\t\t652\t\tsafe\n"
        a = a + "01/10/21 16:05:14\t\t\t26\t\t\t66\t\t536\t\t\t\t56\t\t\t960\t\tsafe\n"
        a = a + "01/10/21 16:05:12\t\t\t25\t\t\t55\t\t55\t\t\t\t58\t\t\t1052\t\tsafe\n"
        self.textEdit_2.setPlainText(a)
        b=self.portInfo = "串口：" + "COM9:USB-SERIRAL" + "\n串口波特率：" + "9600"
        self.textEdit.setPlainText(b)


    def drawing_mode1(self):
        self.modeOneFic = ModeOneWindow(self.gridlayout)
        print("begin draw")
        self.modeOneFic.fig.axes1.cla()
        self.modeOneFic.fig.axes2.cla()
        self.modeOneFic.fig.axes3.cla()
        self.modeOneFic.fig.axes4.cla()
        self.modeOneFic.fig.axes5.cla()

        ax=self.modeOneFic.fig.axes1.plot(self.pass_time, self.temperature, '-ob', color='blue', label='temperature')
        self.modeOneFic.fig.axes2.plot(self.pass_time, self.humidity, '-ob', color='red', label='humidity')
        self.modeOneFic.fig.axes3.plot(self.pass_time, self.third, '-ob', color='green', label='MQ2')
        self.modeOneFic.fig.axes4.plot(self.pass_time, self.forth, '-ob', color='black', label='MQ4')
        self.modeOneFic.fig.axes5.plot(self.pass_time, self.fifth, '-ob', color='orange', label='light')
        plot.xlabel(fontsize=20)
        self.modeOneFic.fig.draw()

        print("--------finish draw--------------")

    def drawing_mode2(self):
        self.modeTwoFic = ModeTwoWindow(self.gridlayout)
        self.modeTwoFic.fig.axes.cla()
        self.modeTwoFic.fig.axes.plot(self.pass_time, self.temperature, '-ob', color='blue', label="temperature")
        self.modeTwoFic.fig.axes.plot(self.pass_time, self.humidity, '-ob', color='red', label="humidity")
        self.modeTwoFic.fig.axes.plot(self.pass_time, self.third, '-ob', color='green', label="concentrate")
        self.modeTwoFic.fig.axes.plot(self.pass_time, self.forth, '-ob', color='black', label="light")
        self.modeTwoFic.fig.axes.set_xlabel("times", fontsize=15)
        self.modeTwoFic.fig.axes.set_ylabel("data", fontsize=15)
        self.modeTwoFic.fig.axes.legend(loc=0, ncol=1)
        self.modeTwoFic.fig.draw()

    @pyqtSlot()
    def on_START_clicked(self):
        # 读取lineEdit中数据
        threading.Thread(target=self.SQL_helper.create_table()).start()
        print('create table')
        try:
            self.getFourCri()
            # 打开串口
            self.ser = My_port(self.name, self.baudrate, self.dataGroupsNum, self.SQL_helper)
            self.ser.getport()  #打开串口
            self.port = self.ser.ser    #得到串口
            if self.port == 0:
                WarningQDialog("CANNOT FIND SERIAL!")
            else:
                self.port.flushInput()  # clear all data in buffer
                print("----------clear all buffer success--------------")
                self.portInfo = "串口：" + self.port.name + "\n串口波特率：" + str(self.port.baudrate)
                self.textEdit.setPlainText(self.portInfo)
                self.PAUSE.setEnabled(True)
                self.START.setEnabled(False)
                self._update_on = 1
                try:
                    self._timer.timeout.connect(self.readPort_Warning)
                    self._timer.start(10)  # after delay
                    self.beginOrEnd = 1
                except:
                    pass
        except:
            WarningQDialog("Please input right number!")

    @pyqtSlot()
    def readPort_Warning(self):
        self.currentTime = str(time.strftime("%H:%M:%S", time.localtime()))
        self.state = 1
        if self.beginOrEnd == 1:
            # 读取数据
            global outTimeNum
            readResult = self.ser.readport(self.currentTime)
            if readResult == 0:  # 读取超时
                outTimeNum += 1
                new_infor = self.currentTime + "\t\t" + "数据读取超时\n"
                self.infor = HEAD + new_infor + self.infor[j_1:len(self.infor)]
                self.textEdit_2.setPlainText(self.infor)
                print("读取数据超时")
                if outTimeNum >= 5:
                    WarningQDialog("PLEASE CHECK YOUR PORT")

            elif readResult == 1:  # 成功读取
                print("-----------read data from serial succeed-----------")
                if self.ser.dataInfor == 'this is GPS data':
                    # 是GPS信号
                    print("-----------GPS information-----------")
                    new_gps = "\n节点" + self.ser._data[0] + "\tGPS定位：" + self.ser._data[1] + ', ' + self.ser._data[2]
                    self.textEdit.append(new_gps)
                    try:
                        threading.Thread(target=self.SQL_helper.writeInto_GPStable(self.ser._data)).start()
                    except:
                        WarningQDialog("Can't write the table " + SQL_Table_name)
                        # self.beginOrEnd = 0
                    print("完成节点GPS信号输入数据库")
                elif self.ser.dataInfor == 'this is sensor data':
                    # 测量值
                    self.temperature.append(self.ser._data[1])
                    self.humidity.append(self.ser._data[2])
                    self.third.append(self.ser._data[3])
                    self.forth.append(self.ser._data[4])
                    self.fifth.append(self.ser._data[5])
                    print(len(self.temperature))
                    self._t += 1
                    self.pass_time.append(self._t)
                    if len(self.temperature) >= 11:
                        print("in if")
                        self.temperature.pop(0)
                        self.humidity.pop(0)
                        self.third.pop(0)
                        self.forth.pop(0)
                        self.fifth.pop(0)
                        self.pass_time.pop(0)
                    else:
                        pass
                    if modeChoice == 1:
                        print("modeOnePlot")
                        self.drawing_mode1()
                        print("modeOnePlotfinish")
                    else:
                        self.drawing_mode2()

                    if self.ifSafe() == 0:
                        self.state = 0

                    # 写入数据库
                    print("SQL")
                    try:
                        threading.Thread(
                            target=self.SQL_helper.writeInto_datatable(self.currentTime, self.state[0],
                                                                       self.ser._data)).start()
                    except:
                        WarningQDialog("Can't write the table " + SQL_Table_name)

                    new_infor = self.scrollOutputInfor(self.state)
                    print("newInfor")
                    self.infor = HEAD + new_infor + self.infor[j_1:len(self.infor)]

                    self.textEdit_2.setPlainText(self.infor)
                    if self.ifSafe() == 0:
                        self.di = QDialog()
                        self.d = dialog.Ui_Dialog()
                        self.d.setupUi(self.di, MESSAGE)
                        self.di.show()

                else:
                    try:
                        new_infor = self.ser.dataInfor
                        self.infor = HEAD + new_infor + self.infor[j_1:len(self.infor)]
                        self.textEdit_2.setPlainText(self.infor)
                    except:
                        new_infor = '无法输出的乱码'
                        self.infor = HEAD + new_infor + self.infor[j_1:len(self.infor)]
                        self.textEdit_2.setPlainText(self.infor)
            elif readResult == -2:
                # 可能丢包
                print("乱码输出")

                try:
                    self.infor = HEAD + self.currentTime + '\t\t' + self.ser.data + "\n" + self.infor[
                                                                                           j_1: len(self.infor)]
                    self.textEdit_2.setPlainText(self.infor)
                except:
                    new_infor = '无法输出的乱码'
                    self.infor = HEAD + new_infor + self.infor[j_1:len(self.infor)]
                    self.textEdit_2.setPlainText(self.infor)
            elif readResult == -1:
                # 没有数据
                pass
            else:
                pass

    @pyqtSlot()
    def on_PAUSE_clicked(self):
        if self._update_on == 1:
            self._update_on = 0
            self.port.close()
            self._timer.timeout.disconnect(self.readPort_Warning)
            threading.Thread(target=self.SQL_helper.close_SQL()).start()
            self.START.setEnabled(True)
            print("------port close success------")
        else:
            pass

    def ModeOneClicked(self):
        self.modeOneFic = ModeOneWindow(self.gridlayout)
        global modeChoice
        modeChoice = 1
        try:
            self.gridlayout.removeWidget(self.modeTwoFic.fig)
            self.gridlayout.removeWidget(self.modeTwoFic.fig_ntb)
            self.modeTwoFic.fig.deleteLater()
            self.modeTwoFic.fig_ntb.deleteLater()
        except:
            pass
        self.Mode2.clicked.connect(self.ModeTwoClicked)

        self.show()

    def ModeTwoClicked(self):
        self.modeTwoFic = ModeTwoWindow(self.gridlayout)
        global modeChoice
        modeChoice = 2
        try:
            self.gridlayout.removeWidget(self.modeOneFic.fig)
            self.gridlayout.removeWidget(self.modeOneFic.fig_ntb)

            self.modeOneFic.fig.deleteLater()
            self.modeOneFic.fig_ntb.deleteLater()
        except:
            pass

        self.Mode1.clicked.connect(self.ModeOneClicked)
        self.show()

    def getFourCri(self):
        self.dataGroupsNum = int(self.NumberComboBox.currentText())
        self.name = str(self.port_list.currentText())
        self.baudrate = int(self.Baudrate_comboBox.currentText())

    @staticmethod
    def get_port_list():
        # get all the COM port currently
        com_list = []
        port_list = serial.tools.list_ports.comports()
        for port in port_list:
            com_list.append(port[0] + ':USB-SERIAL')
        return com_list

    def ifSafe(self):
        predictNum = self.ser._data[1:len(self.ser._data)]
        predictNum = [int(predictNum) for predictNum in predictNum]
        self.state = self.neuralNetwork.predict(predictNum)
        print('*********predict value:' + str(self.state[0]))
        if self.state[0] > 0.9:
            state = 1
        else:
            state = 0
        print('go out ifsafe')
        return state

    def scrollOutputInfor(self, flags):
        new_infor0 = self.currentTime
        i = 0
        while i < self.dataGroupsNum:
            new_infor0 += '\t\t' + str(self.ser._data[i])
            i += 1
        if not flags:
            new_infor = new_infor0 + "\t\tDANGER\n"
        else:
            new_infor = new_infor0 + "\t\tsafe\n"
        return new_infor


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = AppWindow()
    win.show()
    sys.exit(app.exec_())
