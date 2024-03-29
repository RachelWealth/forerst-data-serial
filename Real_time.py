# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Real-timr.ui'
#
# Created by: PyQt5 UI code generator 5.15.1
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1300, 810)
        MainWindow.setMinimumSize(QtCore.QSize(1300, 810))
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet("QMainWindow{\n"
"    opacity:0.5;\n"
"}")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setStyleSheet("")
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.splitter_4 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_4.setMaximumSize(QtCore.QSize(16777215, 220))
        self.splitter_4.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_4.setObjectName("splitter_4")
        self.textEdit = QtWidgets.QTextEdit(self.splitter_4)
        self.textEdit.setMaximumSize(QtCore.QSize(200, 220))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.textEdit.setFont(font)
        self.textEdit.setTabletTracking(False)
        self.textEdit.setStyleSheet("QTextEdit{\n"
"    border-radius:30px;\n"
"    backgroud:white;\n"
"    font: 12pt \"Times New Roman\";\n"
"}")
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.textEdit_2 = QtWidgets.QTextEdit(self.splitter_4)
        self.textEdit_2.setMaximumSize(QtCore.QSize(16777215, 220))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.textEdit_2.setFont(font)
        self.textEdit_2.setStyleSheet("QTextEdit{\n"
"    font: 12pt \"Times New Roman\";\n"
"    border-radius:30px;\n"
"    backgroud:white;\n"
"}")
        self.textEdit_2.setReadOnly(True)
        self.textEdit_2.setObjectName("textEdit_2")
        self.gridLayout.addWidget(self.splitter_4, 1, 0, 1, 1)
        self.splitter_2 = QtWidgets.QSplitter(self.centralwidget)
        self.splitter_2.setOrientation(QtCore.Qt.Horizontal)
        self.splitter_2.setObjectName("splitter_2")
        self.splitter = QtWidgets.QSplitter(self.splitter_2)
        self.splitter.setOrientation(QtCore.Qt.Vertical)
        self.splitter.setObjectName("splitter")
        self.START = QtWidgets.QPushButton(self.splitter)
        self.START.setMaximumSize(QtCore.QSize(200, 16777215))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.START.setFont(font)
        self.START.setStyleSheet("QPushButton{\n"
"    background-color:rgb(105, 255, 35);\n"
"    border-radius:15px;\n"
"    font: 20pt \"Times New Roman\";\n"
"}\n"
"QPushButton:hover{\n"
"    background-color:rgb(255, 170, 0);\n"
"}")
        self.START.setAutoRepeat(False)
        self.START.setObjectName("START")
        self.PAUSE = QtWidgets.QPushButton(self.splitter)
        self.PAUSE.setMaximumSize(QtCore.QSize(200, 16777215))
        self.PAUSE.setStyleSheet("QPushButton{\n"
"    background-color:rgb(255, 49, 49);\n"
"    border-radius:15px;\n"
"    font: 20pt \"Times New Roman\";\n"
"}\n"
"QPushButton:hover{\n"
"    background-color:rgb(0, 0, 255);\n"
"}")
        self.PAUSE.setObjectName("PAUSE")
        self.Mode1 = QtWidgets.QPushButton(self.splitter)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.Mode1.setFont(font)
        self.Mode1.setStyleSheet("QPushBuuton{\n"
"    font: 15pt \"Times New Roman\";\n"
"}")
        self.Mode1.setObjectName("Mode1")
        self.Mode2 = QtWidgets.QPushButton(self.splitter)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.Mode2.setFont(font)
        self.Mode2.setStyleSheet("QPushBuuton{\n"
"    font: 15pt \"Times New Roman\";\n"
"}")
        self.Mode2.setObjectName("Mode2")
        self.label = QtWidgets.QLabel(self.splitter)
        self.label.setMaximumSize(QtCore.QSize(200, 45))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setObjectName("label")
        self.port_list = QtWidgets.QComboBox(self.splitter)
        self.port_list.setMinimumSize(QtCore.QSize(150, 0))
        self.port_list.setMaximumSize(QtCore.QSize(70, 40))
        self.port_list.setObjectName("port_list")
        self.label_2 = QtWidgets.QLabel(self.splitter)
        self.label_2.setMaximumSize(QtCore.QSize(200, 45))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.Baudrate_comboBox = QtWidgets.QComboBox(self.splitter)
        self.Baudrate_comboBox.setMaximumSize(QtCore.QSize(100, 30))
        self.Baudrate_comboBox.setObjectName("Baudrate_comboBox")
        self.label_4 = QtWidgets.QLabel(self.splitter)
        self.label_4.setMaximumSize(QtCore.QSize(100, 45))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.NumberComboBox = QtWidgets.QComboBox(self.splitter)
        self.NumberComboBox.setMaximumSize(QtCore.QSize(100, 45))
        self.NumberComboBox.setStyleSheet("NumberComboBox{\n"
"    background-color: rgb(255, 255, 255);\n"
"}")
        self.NumberComboBox.setObjectName("NumberComboBox")
        self.Real_time_graph = QtWidgets.QGroupBox(self.splitter_2)
        self.Real_time_graph.setMinimumSize(QtCore.QSize(391, 250))
        self.Real_time_graph.setObjectName("Real_time_graph")
        self.gridLayout.addWidget(self.splitter_2, 0, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1300, 26))
        self.menubar.setObjectName("menubar")
        self.menuFilws = QtWidgets.QMenu(self.menubar)
        self.menuFilws.setObjectName("menuFilws")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFilws.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.START.setText(_translate("MainWindow", "START"))
        self.PAUSE.setText(_translate("MainWindow", "PAUSE"))
        self.Mode1.setText(_translate("MainWindow", "MODE1"))
        self.Mode2.setText(_translate("MainWindow", "MODE2"))
        self.label.setText(_translate("MainWindow", "Port："))
        self.label_2.setText(_translate("MainWindow", "Buadrate:"))
        self.label_4.setText(_translate("MainWindow", "Groups:"))
        self.Real_time_graph.setTitle(_translate("MainWindow", "Dynamic"))
        self.menuFilws.setTitle(_translate("MainWindow", "Files"))
