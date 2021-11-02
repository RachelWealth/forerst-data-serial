# -*- coding: utf-8 -*-
import threading

import serial
# noinspection PyBroadException
from datetime import datetime

from WriteIntoSQL import WriteIntoSQL

now = datetime.now()
SQL_Table_name = 'time' + now.strftime("%Y%m%d")


# noinspection PyAttributeOutsideInit,PyBroadException
class My_port():
    def __init__(self, name, baudrate, dataGroupsNum,SQL_helper):
        self.name = name
        self.baudrate = baudrate
        self.timeout = 1
        self.data = b''
        self._data = []
        self.ser = 0
        self.singleType = 0  # 0位不可分析信号（乱码），1为传感器数据，2为GPS数据
        self.point = []
        self.dataGroupsNum = dataGroupsNum
        self.SQL_helper = SQL_helper
        self.dataInfor = ''
        self.currentTime = ''

    def isOpenport(self):
        if self.ser.isOpen():
            print(self.name + " is open")
            return 1
        else:
            print(self.name + " is not open")
            return 0

    def getport(self):
        try:
            self.ser = serial.Serial(
                port=self.name,
                baudrate=self.baudrate,
                timeout=self.timeout,
                parity=serial.PARITY_ODD,  # 校验位
                stopbits=serial.STOPBITS_TWO,  # 停止位
                bytesize=serial.SEVENBITS  # 数据位
            )
        except:
            print("cannot find serial!")
            self.ser = 0

    def readport(self, currentTime):
        self.currentTime = currentTime
        try:
            n = self.ser.inWaiting()
            if n != 0:
                self.data = self.ser.readline()
                print(self.data)
                print("---read data from serial finish, analyze the data...")

                if self.data == b'':
                    print("get1")
                    return 0
                else:
                    print("begin analyzing...")
                    if self.analyzeData() == -2:
                        print("乱码或者丢包")
                        return -2
                    else:
                        return 1
            else:
                return -1
        except IOError:
            return -3

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, value):
        self._data = value

    def getEveryPortData(self):
        print("getEveryPortData")
        self._data = self.data.split()
        i = 0

        while i < self.dataGroupsNum + 1:
            self._data[i] = self._data[i].decode('utf-8')
            i += 1
        print("getEveryPortData finish")

    def analyzeData(self):
        self.getEveryPortData()
        # 查找GPS表，查看是否有该节点信息
        self.sql = 'SELECT node FROM ' + self.SQL_helper.GPS_table_name + ' WHERE node=?'
        self.SQL_helper.open_SQL()
        self.SQL_helper.cursor_2.execute(self.sql,(self._data[0],))
        num = len(list(self.SQL_helper.cursor_2))
        print("------- 游标返回行数：" + str(num))
        if num==0:
            # 没有这个节点，是GPS信号
            GPSInforNum = 3
            i = 1
            n = len(self._data)
            if n >= 3:
                self.dataInfor = 'this is GPS data'
            else:
                self.dataInfor = 'GPS data error!'
                return 1
        else:
            #   有这个节点则说明是传感器数据
            n = len(self._data)
            i = 1
            if n == self.dataGroupsNum + 1:
                self.dataInfor = 'this is sensor data'
                return 1
            else:
                self.dataInfor = 'sensor data error'
                return 1
