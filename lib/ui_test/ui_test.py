from PyQt5.QtCore import QRect, QCoreApplication, QMetaObject
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QTableView, QPushButton, QComboBox, QLabel, QListWidget, QMenuBar, QStatusBar, QAction, QHeaderView, QAbstractItemView, QTableView, QMessageBox, QInputDialog, QLineEdit
import sys
import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Hanshow AP Config Toolbox")
        MainWindow.resize(900, 650)
        MainWindow.setStyleSheet('QWidget {font: "Roboto Mono"}')
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.tableWidget = QTableView(self.centralwidget)
        self.tableWidget.setGeometry(QRect(30, 20, 511, 560))
        self.tableWidget.setObjectName("tableWidget")
        self.pushButton = QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QRect(700, 40, 75, 24))
        self.pushButton.setObjectName("pushButton")
        self.selectBox = QComboBox(self.centralwidget)
        self.selectBox.setGeometry(QRect(688, 80, 100, 24))
        self.selectBox.setObjectName("selectBox")
        self.configButton = QPushButton(self.centralwidget)
        self.configButton.setGeometry(QRect(650, 120, 75, 24))
        self.configButton.setObjectName("configButton")
        _translate = QCoreApplication.translate
        self.configButton.setText(_translate("MainWindow", "Edit"))
        self.configButton.setVisible(False)
        self.reloadButton = QPushButton(self.centralwidget)
        self.reloadButton.setGeometry(QRect(750, 120, 75, 24))
        self.reloadButton.setObjectName("reloadButton")
        self.reloadButton.setText(_translate("MainWindow", "Reload"))
        self.reloadButton.setVisible(False)
        self.alert = QLabel(self.centralwidget)
        self.alert.setGeometry(QRect(30, 580, 511, 24))
        self.alert.setObjectName("disableConnection")
        self.config = QListWidget(self.centralwidget)
        self.config.setGeometry(QRect(550, 180, 340, 380))
        self.config.setObjectName("configInfo")

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.model = QStandardItemModel(0, 2)
        self.model.setHorizontalHeaderLabels(['Address IP', 'Address Mac'])
        self.tableWidget.setModel(self.model)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setEditTriggers(QTableView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.msgBox = QMessageBox()
        self.retranslateUi(MainWindow)
        self.pushButton.released.connect(self.slotAdd)
        QMetaObject.connectSlotsByName(MainWindow)

        self.slotAdd()

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Hanshow AP config Toolbox"))
        MainWindow.setWindowIcon(QIcon('style/icon.ico'))
        self.pushButton.setText(_translate("MainWindow", "Get All AP"))

        self.alert.setText(_translate(
            "MainWindow", "Disable All Your VPN Connections Before Using"))
        self.alert.setStyleSheet("color: red;")

    def slotAdd(self):
        self.pushButton.setEnabled(False)
        # This is where you would implement the logic for what happens when the button is pressed.
        self.pushButton.setEnabled(True)
