# -*- coding: utf-8 -*-
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.

from PyQt5.QtCore import QRect, QCoreApplication, QMetaObject,Qt
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QWidget, QTableView, QPushButton, QComboBox, QLabel, QListWidget, QMenuBar, QStatusBar, QAction, QHeaderView, QAbstractItemView, QTableView, QMessageBox, QInputDialog, QLineEdit
import paramiko
import sys
import os
from subprocess import Popen
from time import sleep


sys.path.append(os.path.dirname(__file__))
from utils import *
from model import *

#####Version1.2 add
import json

GRP_CONFIG = "DEFAULT"
CONFIG = []
VPN = False
df = ''
IP_LIST = []


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
        self.configButton.clicked.connect(self.open_config_file)
        self.reloadButton = QPushButton(self.centralwidget)
        self.reloadButton.setGeometry(QRect(750, 120, 75, 24))
        self.reloadButton.setObjectName("reloadButton")
        _translate = QCoreApplication.translate
        self.reloadButton.setText(_translate("MainWindow", "Reload"))
        self.reloadButton.setVisible(False)
        self.reloadButton.clicked.connect(self.grpChange)
        configs = get_config()
        configs.insert(0, GRP_CONFIG)
        configs.remove('readme.txt')
        self.selectBox.addItems(configs)
        self.selectBox.currentIndexChanged.connect(self.grpChange)
        self.alert = QLabel(self.centralwidget)
        self.alert.setGeometry(QRect(30, 580, 511, 24))
        self.config = QListWidget(self.centralwidget)  # 确保初始化 self.config
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
        # self.model = QStandardItemModel(0, 2) 
        self.model = QStandardItemModel(0, 3)  # 修改列数
        # self.model.setHorizontalHeaderLabels(['Address IP', 'Address Mac'])
        self.model.setHorizontalHeaderLabels(['Select', 'Address IP', 'Address Mac']) #多加一个复选框
        self.tableWidget.setModel(self.model)
        ################################################
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setSelectionMode(QAbstractItemView.MultiSelection)  # 允许多选
        self.tableWidget.setEditTriggers(QTableView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        ################################################
        tool = self.addToolBar("File")
        self.action_detail = QAction("Detail", self)
        self.action_config = QAction("Config", self)
        self.action_delete = QAction("Delete", self)
        self.action_version = QAction("Version Check", self)
        self.action_descript = QAction("Descript Check", self)
        tool.addAction(self.action_detail)
        tool.addAction(self.action_config)
        tool.addAction(self.action_delete)
        tool.addAction(self.action_version)
        tool.addAction(self.action_descript)
        tool.actionTriggered[QAction].connect(self.processtrigger)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tableWidget.setEditTriggers(QTableView.NoEditTriggers)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.msgBox = QMessageBox()
        self.retranslateUi(MainWindow)
        self.pushButton.released.connect(self.slotAdd)  # type: ignore
        QMetaObject.connectSlotsByName(MainWindow)

        self.slotAdd()

    def processtrigger(self, action):
        if action.text() == "Detail":
            r = self.tableWidget.selectionModel().selectedRows()
            if r:
                index_ip = self.tableWidget.model().index(self.tableWidget.currentIndex().row(), 0)
                index_mac = self.tableWidget.model().index(index_ip.row(), 1)
                data_ip = self.tableWidget.model().data(index_ip)
                data_mac = self.tableWidget.model().data(index_mac)
                data = [data_ip, data_mac]
                print(data)
                self.launchPopup(data_ip, data_mac)
        if action.text() == "Config":
            r = self.tableWidget.selectionModel().selectedRows()
            if r:
                index_ip = self.tableWidget.model().index(self.tableWidget.currentIndex().row(), 0)
                index_mac = self.tableWidget.model().index(index_ip.row(), 1)
                data_ip = self.tableWidget.model().data(index_ip)
                data_mac = self.tableWidget.model().data(index_mac)
                data = [data_ip, data_mac]
                print(data)
                self.launchPopup(data_ip, data_mac)
        if action.text() == "Delete":
            r = self.tableWidget.selectionModel().selectedRows()
            if r:
                index = self.tableWidget.currentIndex()
                print(index.row())
                self.model.removeRow(index.row())

        if action.text() == "Version Check":
            if IP_LIST:
                version = []
                res = ["AP Version Check Result:", "IP\t\t\tVersion"]
                for ip in IP_LIST:
                    sleep(0.2)
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    try:
                        ssh.connect(ip, username="root", password="hanshow-imx6")
                        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("/home/elinker/bin/elinker -v")
                        version.append(ssh_stdout.read().decode('utf-8'))
                    except:
                        version.append("ERROR")
                        print("Error when connect to : ", ip)
                for i, v in zip(IP_LIST, version):
                    res.append(i + '\t\t' + v)
                self.msgBox.setIcon(QMessageBox().Information)
                self.msgBox.setText("\n".join(res))
                self.msgBox.setWindowTitle("AP Version")
                self.msgBox.setWindowIcon(QIcon('style/icon.ico'))
                self.msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                returnValue = self.msgBox.exec()
                if returnValue == QMessageBox.Ok:
                    return

        if action.text() == "Descript Check":
            if IP_LIST:
                descript = []
                res = ["Description Check Result:", "IP\t\t\tDescription"]
                for ip in IP_LIST:
                    sleep(0.2)
                    ssh = paramiko.SSHClient()
                    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    try:
                        ssh.connect(ip, username="root", password="hanshow-imx6")
                        ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command("cat /tmp/.config.ini |grep descript")
                        d = ssh_stdout.read().decode('utf-8').split('=')[1]
                        descript.append(d)
                    except:
                        descript.append("ERROR")
                        print("Error when connect to : ", ip)
                for i, v in zip(IP_LIST, descript):
                    res.append(i + '\t\t' + v)
                self.msgBox.setIcon(QMessageBox().Information)
                self.msgBox.setText("\n".join(res))
                self.msgBox.setWindowTitle("AP Description")
                self.msgBox.setWindowIcon(QIcon('style/icon.ico'))
                self.msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
                returnValue = self.msgBox.exec()
                if returnValue == QMessageBox.Ok:
                    return


    def grpChange(self):
        global GRP_CONFIG, CONFIG
        GRP_CONFIG = self.selectBox.currentText()
        self.reloadButton.setEnabled(False)
        if GRP_CONFIG != "DEFAULT":
            CONFIG = get_file_config(f"config/{GRP_CONFIG}")
            self.read_config_file()
            self.configButton.setVisible(True)
            self.reloadButton.setVisible(True)
        else:
            self.config.clear()
            self.configButton.setVisible(False)
            self.reloadButton.setVisible(False)
            CONFIG = []

    def read_config_file(self):
        self.config.clear()
        self.config.addItem("Settings to change manually: ")
        for i, conf in enumerate(CONFIG):
            if conf[0] == "!":
                type = conf.split("=")[0].split("!")[1].strip()
                value = conf.split("=")[1]
                self.config.addItem(TRANSLATION[type] + value)
        self.config.addItem("")
        self.config.addItem("Settings do not need to be changed: ")
        for i, conf in enumerate(CONFIG):
            if conf[0] != "!":
                type = conf.split("=")[0].strip()
                value = conf.split("=")[1]
                self.config.addItem(TRANSLATION[type] + value)

    def open_config_file(self):
        print("open file")
        self.msgBox.setIcon(QMessageBox().Warning)
        self.msgBox.setWindowIcon(QIcon('style/icon.ico'))
        self.msgBox.setText(WARNING)
        self.msgBox.setWindowTitle("Important Information")
        self.msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        returnValue = self.msgBox.exec()
        if returnValue == QMessageBox.Ok:
            Popen(f'notepad ".\config\{GRP_CONFIG}"', shell=False)
            self.reloadButton.setEnabled(True)

    def slotAdd(self):
        self.pushButton.setEnabled(False)
        clear_arp_cache()
        self.getAP = GetApTheard()
        self.getAP._sum.connect(self.update_tab)
        self.getAP.start()
        global VPN
        if VPN == True:
            VPN = False
            self.msgBox.setIcon(QMessageBox().Warning)
            self.msgBox.setText(f"Please disable all your VPN connections!")
            self.msgBox.setWindowTitle("Error")
            self.msgBox.setWindowIcon(QIcon('style/icon.ico'))
            self.msgBox.setStandardButtons(QMessageBox.Ok)
            returnValue = self.msgBox.exec()
            if returnValue == QMessageBox.Ok:
                return

    def update_tab(self, r):
        global IP_LIST
        i = 0
        for ip, mac in df:
            select_item = QStandardItem()
            select_item.setCheckable(True)  # 设置为可勾选，最左边的那列复选
            select_item.setCheckState(Qt.Unchecked)
            ip_item = QStandardItem(ip)
            mac_item = QStandardItem(mac.replace('-', ':').upper())
            self.model.setItem(i, 0, mac_item)
            self.model.setItem(i, 1, ip_item)
            self.model.setItem(i, 2, mac_item)
            i = i+1
            IP_LIST.append(ip)
        self.pushButton.setEnabled(True)
        print(IP_LIST)

    # def update_tab(self, r):
    # global IP_LIST
    # i = 0
    # for k, v in df:
    #     select_item = QStandardItem()
    #     select_item.setCheckable(True)
    #     select_item.setCheckState(Qt.Unchecked)
    #     ip_item = QStandardItem(k)
    #     mac_item = QStandardItem(v.replace('-', ':').upper())
    #     self.model.setItem(i, 0, select_item)
    #     self.model.setItem(i, 1, ip_item)
    #     self.model.setItem(i, 2, mac_item)
    #     i = i + 1
    #     IP_LIST.append(k)
    # self.pushButton.setEnabled(True)
    # print(IP_LIST)

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        MainWindow.setWindowTitle(_translate(
            "MainWindow", "Hanshow AP config Toolbox"))
        MainWindow.setWindowIcon(QIcon('style/icon.ico'))
        self.pushButton.setText(_translate("MainWindow", "Get All AP"))

        self.alert.setText(_translate(
            "MainWindow", "Disable All Your VPN Connections Before Using"))
        self.alert.setStyleSheet("color: red;")

    def change_pwd(self, value=""):
        global CONFIG
        pwd, ok = QInputDialog.getText(
            self, "Password for admin", "Password(blank for not change): ", QLineEdit.Normal, value)
        if not ok:
            return 1
        if pwd:
            self.config.addItem("New password: " + pwd)
            self.config.setStyleSheet("color: red;")
        if not pwd:
            self.config.addItem("Password: admin")
            self.config.setStyleSheet("color: red;")
            pwd = "admin"

        CONFIG.append(
            f"cgi -a manager_passwd={encrypt_md5(f'admin:need input passwd:{pwd}')}")

    def change_ip(self, ip_add=""):
        global CONFIG
        ip, ok = QInputDialog.getText(
            self, "IP Addr", "IP Addr(blank for DHCP): ", QLineEdit.Normal, ip_add)
        if not ok:
            return 1
        if not ip:
            net_dhcp = "true"
            self.config.addItem("No IP. Using DHCP")
            self.config.setStyleSheet("color: red;")
            CONFIG.append(f"cgi -a net_dhcp={net_dhcp}")
        if ip:
            net_dhcp = "false"
            if isIP(ip) == False:
                self.config.clear()
                self.config.addItem("Not a IP format")
                self.config.setStyleSheet("color: red;")
                return 1
            self.config.addItem("IP address: " + ip)
            self.config.setStyleSheet("color: red;")
            CONFIG.append(f"cgi -a net_dhcp={net_dhcp};cgi -a net_ipaddr={ip}")
        return [net_dhcp, ip]

    def change_mask(self, val=""):
        global CONFIG
        mask, ok = QInputDialog.getText(
            self, "Netmask", "Netmask: ", QLineEdit.Normal, val)
        if not ok:
            return 1
        if not mask:
            self.config.clear()
            self.config.addItem("Not a IP format")
            self.config.setStyleSheet("color: red;")
            return 1
        if mask:
            if isIP(mask) == False:
                self.config.clear()
                self.config.addItem("Not a IP format")
                self.config.setStyleSheet("color: red;")
                return 1
            self.config.addItem("Netmask: " + mask)
            self.config.setStyleSheet("color: red;")
            CONFIG.append(f"cgi -a net_netmask={mask}")

    def change_gateway(self, gate=""):
        global CONFIG
        gateway, ok = QInputDialog.getText(
            self, "Gateway", "Gateway: ", QLineEdit.Normal, gate)
        if not ok:
            return 1
        if not gateway or isIP(gateway) == False:
            self.config.clear()
            self.config.addItem("Not a IP format")
            self.config.setStyleSheet("color: red;")
            return 1
        if gateway:
            self.config.addItem("Gateway: " + gateway)
            self.config.setStyleSheet("color: red;")
            CONFIG.append(f"cgi -a net_router={gateway}")

    def change_dns1(self, dns=''):
        global CONFIG
        dns1, ok = QInputDialog.getText(
            self, "DNS 1", "DNS 1(blank for no using DNS): ", QLineEdit.Normal, dns)
        if not ok:
            return 1
        if not dns1:
            self.config.addItem("No DNS Addr 1")
            self.config.setStyleSheet("color: red;")
        if dns1:
            if isIP(dns1) == False:
                self.config.clear()
                self.config.addItem("Not a IP format")
                self.config.setStyleSheet("color: red;")
                return 1
            self.config.addItem("DNS 1: " + dns1)
            self.config.setStyleSheet("color: red;")
            CONFIG.append(f"cgi -a net_dns1={dns1}")

    def change_dns2(self, dns=''):
        global CONFIG
        dns2, ok = QInputDialog.getText(
            self, "DNS 2", "DNS 2(blank for no using DNS 2): ", QLineEdit.Normal, dns)
        if not ok:
            return 1
        if not dns2:
            self.config.addItem("No DNS Addr 2")
            self.config.setStyleSheet("color: red;")
        if dns2 and ok:
            if isIP(dns2) == False:
                self.config.clear()
                self.config.addItem("Not a IP format")
                self.config.setStyleSheet("color: red;")
                return 1
            self.config.addItem("DNS 2: " + dns2)
            self.config.setStyleSheet("color: red;")
            CONFIG.append(f"cgi -a net_dns2={dns2}")

    def change_ewip(self, ip=""):
        global CONFIG
        ew_ip, ok = QInputDialog.getText(
            self, "ESL-working Addr", "EW Address(blank for using auto search): ", QLineEdit.Normal, ip)
        if not ok:
            return 1
        if not ew_ip:
            ew_udp = "true"
            self.config.addItem("ESL-Working Addr: Auto")
            self.config.setStyleSheet("color: red;")
            CONFIG.append(f"cgi -a ew_udp={ew_udp}")
        if ew_ip:
            ew_udp = "false"
            self.config.addItem("ESL-Working Addr: " + ew_ip)
            self.config.setStyleSheet("color: red;")
            CONFIG.append(f"cgi -a ew_udp={ew_udp};cgi -a ew_ipaddr={ew_ip}")
        return ew_udp

    def change_ewport(self, port="37021"):
        global CONFIG
        ew_port, ok = QInputDialog.getText(
            self, "ESL-working Port", "EW Port(blank for 37021): ", QLineEdit.Normal, port)
        if not ok:
            return 1
        if not ew_port:
            ew_port = "37021"
        if ew_port:
            self.config.addItem("ESL-Working Port: " + ew_port)
            self.config.setStyleSheet("color: red;")
        CONFIG.append(f"cgi -a ew_port={ew_port}")

    def change_ewssl(self, ssl=False):
        global CONFIG
        ew_ssl, ok = QInputDialog.getItem(
            self, "ESL-Working SSL", "ESL-Working SSL?", ['false', 'true'], 0, ssl)
        if not ok:
            return 1
        if ew_ssl:
            self.config.addItem("ESL-Working SSL: " + ew_ssl)
            self.config.setStyleSheet("color: red;")
            CONFIG.append(f"cgi -a ew_ssl={ew_ssl}")

    def change_test(self, test=False):
        global CONFIG
        rul_enable, ok = QInputDialog.getItem(
            self, "Mode Test", "Mode Test Enable?", ['true', 'false'], 0, test)
        if not ok:
            return 1
        if rul_enable:
            self.config.addItem("Mode Test Enable: " + rul_enable)
            self.config.setStyleSheet("color: red;")
            CONFIG.append(
                f"cgi -a rul_enable={rul_enable};cgi -a rul_id=52-56-78-53;cgi -a rul_channel=50")

    def change_descript(self, descript=""):
        global CONFIG
        description, ok = QInputDialog.getText(
            self, "Description(optional)", "Description(optional)", QLineEdit.Normal, descript)
        if not ok:
            return 1
        if not description:
            self.config.addItem("Description: None")
            self.config.setStyleSheet("color: red;")
        if description:
            # # 将单引号替换为双引号,但行不通，加上就错,或许可以试试json转义库
            # description = description.replace("'", "\"")
            self.config.addItem("Description: " + description)
            self.config.setStyleSheet("color: red;")
            # 使用双引号将描述包含起来
            CONFIG.append(f'cgi -a descript="{description}"')


    def launchPopup(self):
        #########################################################
        selected_indexes = self.tableWidget.selectionModel().selectedRows()
        if not selected_indexes:
            self.msgBox.setIcon(QMessageBox.Warning)
            self.msgBox.setText("No AP selected!")
            self.msgBox.setWindowTitle("Warning")
            self.msgBox.setStandardButtons(QMessageBox.Ok)
            self.msgBox.exec()
            return

        # 获取用户输入的新 IP 和描述
        new_ip_range, ok = QInputDialog.getText(
            self, "New IP Range", "Enter new IP range (e.g., 10.32.26.57-59):", QLineEdit.Normal)
        if not ok or not new_ip_range:
            return

        new_description, ok = QInputDialog.getText(
            self, "New Description", "Enter new description (e.g., ITM AP A-D):", QLineEdit.Normal)
        if not ok or not new_description:
            return

        # 解析 IP 范围
        ip_base, ip_range = new_ip_range.rsplit('.', 1)
        ip_start, ip_end = map(int, ip_range.split('-'))

        # 解析描述
        if '-' in new_description:
            desc_base, desc_range = new_description.rsplit(' ', 1)
            desc_start, desc_end = desc_range.split('-')
            desc_letters = [chr(i) for i in range(ord(desc_start), ord(desc_end) + 1)]
        else:
            desc_base = new_description
            desc_letters = [None] * len(selected_indexes)

        # 为选中的 AP 分配新配置
        for i, index in enumerate(selected_indexes):
            ip = f"{ip_base}.{ip_start + i}"
            desc = f"{desc_base} {desc_letters[i]}" if desc_letters[i] else desc_base
            row = index.row()
            self.model.setData(self.model.index(row, 1), ip)
            self.model.setData(self.model.index(row, 2), desc)

            # 更新配置
            CONFIG.append(f'cgi -a net_ipaddr={ip}')
            CONFIG.append(f'cgi -a descript="{desc}"')

        # 应用配置到选中的 AP
        for index in selected_indexes:
            ip = self.model.data(self.model.index(index.row(), 1))
            ap_mac = self.model.data(self.model.index(index.row(), 2))
            self.apply_config(ip, ap_mac)


        ##########################################################################
    def apply_config(self, ap_ip, ap_mac):
        print(ap_ip,ap_mac)
        clear_arp_cache()  # 清除arp缓存
        global GRP_CONFIG, CONFIG
        if GRP_CONFIG != "DEFAULT":
            CONFIG = get_file_config(f"config/{GRP_CONFIG}")
        else:
            CONFIG = []
        self.config.clear()
        self.config.addItem("---------------------")
        self.config.addItem(f"{ap_mac.replace('-',':')}")
        self.config.addItem("---------------------")
        self.config.setStyleSheet("color: red;")
        if GRP_CONFIG == "DEFAULT":  # 默认配置处理
            if self.change_pwd() == 1:
                return
            need_change_ip = self.change_ip()[0]
            if need_change_ip == "false":
                if self.change_mask() == 1:
                    return
                if self.change_gateway() == 1:
                    return
                if self.change_dns1() == 1:
                    return
                if self.change_dns2() == 1:
                    return
            elif need_change_ip == 1:
                return
            need_change_ewip = self.change_ewip()
            if need_change_ewip == "false":
                if self.change_ewport() == 1:
                    return
                if self.change_ewssl() == 1:
                    return
            elif need_change_ewip == 1:
                return
            if self.change_test() == 1:
                return
            if self.change_descript() == 1:
                return
        else:
            print(CONFIG)
            for i, conf in enumerate(CONFIG):
                print(i, conf)
                if conf[0] == "!":  # 处理要更改的配置
                    type = conf.split("=")[0].split("!")[1].strip()
                    value = conf.split("=")[1]
                    if type == "manager_passwd":
                        if self.change_pwd(value) == 1:
                            return
                    if type == "net_ipaddr":
                        ip = self.change_ip(value)[1]
                        if ip == 1:
                            return
                    if type == "net_netmask":
                        if self.change_mask(value) == 1:
                            return
                    if type == "net_router":
                        if self.change_gateway(value) == 1:
                            return
                    if type == "net_dns1":
                        if self.change_dns1(value) == 1:
                            return
                    if type == "net_dns2":
                        if self.change_dns1(value) == 1:
                            return
                    if type == "ew_ipaddr":
                        if self.change_ewip(value) == 1:
                            return
                    if type == "ew_port":
                        if self.change_ewport(value) == 1:
                            return
                    if type == "ew_ssl":
                        if self.change_ewssl(value) == 1:
                            return
                    if type == "rul_enable":
                        if self.change_test(value) == 1:
                            return
                    if type == "descript":
                        if self.change_descript(value) == 1:
                            return
                    CONFIG[i] = ''
                else:
                    type = conf.split("=")[0].strip()
                    if GRP_CONFIG == "SystemeU":
                        if type == "net_netmask":
                            CONFIG[i] = "net_netmask=255.255.252.0"
                        if type == "ew_ipaddr":
                            CONFIG[i] = f"ew_ipaddr={range_of_ip(ip,'255.255.252.0')[1]}"
                        if type == "net_router":
                            CONFIG[i] = f"net_router={range_of_ip(ip,'255.255.252.0')[0]}"
            CONFIG = [i for i in CONFIG if i != '']
            for i, conf in enumerate(CONFIG):  # 给固定配置加前缀cgi -a
                type = conf.split("=")[0].strip()
                value = conf.split("=")[1]
                if "cgi -a " not in conf:
                    CONFIG[i] = "cgi -a " + CONFIG[i]
                    self.config.addItem(TRANSLATION[type] + value)
        if 'cgi -a rul_enable=true' in CONFIG:
            CONFIG.append('cgi -a rul_id=52-56-78-53;cgi -a rul_channel=50')
        print(CONFIG)

        self.msgBox.setIcon(QMessageBox().Warning)
        self.msgBox.setText(
            f"Do you want to set these configurations to this AP ({ap_mac})?")
        self.msgBox.setWindowTitle("Are You Sure??")
        self.msgBox.setWindowIcon(QIcon('style/icon.ico'))
        self.msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
        returnValue = self.msgBox.exec()
        if returnValue == QMessageBox.Ok:
            self.msgBox = QMessageBox()
            self.msgBox.setIcon(QMessageBox().Warning)
            self.msgBox.setText(
                f"Do you want to restart AP ({ap_mac})? (Needed if network configuration changed)")
            self.msgBox.setWindowTitle("Are You Sure??")
            self.msgBox.setWindowIcon(QIcon('style/icon.ico'))
            self.msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
            returnValue = self.msgBox.exec()
            if returnValue == QMessageBox.Ok:
                command = ';'.join(CONFIG)+";sync;cgi -e;reboot;"
            else:
                command = ';'.join(CONFIG)+";sync;cgi -e;"
            print(command)
        # commande = "cgi -e"
        ip = ap_ip
        print(ip)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(ip, username="root", password="hanshow-imx6")
            ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
            print(ssh_stdout.read().decode('utf-8'))
        except:
            print("Error when connect to : ", ip)


class GetApTheard(QThread):
    """该线程用于计算耗时的累加操作"""
    _sum = pyqtSignal(str)  # 信号类型 str

    def __init__(self):
        super().__init__()

    def run(self):
        global df, VPN
        try:
            df = get_ap().values.tolist()
        except:
            VPN = True
        self._sum.emit("success")  # 计算结果完成后，发送结果
