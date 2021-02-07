from PyQt5 import QtWidgets, uic, QtSerialPort, QtCore
import os
import sys
from PyQt5.QtWidgets import QFileDialog

import paramiko
from paramiko import SSHClient


class control_server(QtWidgets.QMainWindow):
    def __init__(self):
        super(control_server, self).__init__()
        uic.loadUi('mainwindow.ui', self)
        self.clouds.clicked.connect(self.shutdownClouds)
        self.pihole.clicked.connect(self.shutdownPihole)
        self.unms.clicked.connect(self.shutdownUnms)

        self.clientPihole = SSHClient()
        self.clientClouds = SSHClient()
        self.clientUnms = SSHClient()
        self.clientPihole.load_system_host_keys()
        self.clientPihole.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.clientClouds.load_system_host_keys()
        self.clientClouds.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.clientUnms.load_system_host_keys()
        self.clientUnms.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        self.command = "sudo shutdown -h now"
        try:
            self.clientPihole.connect(
                '192.168.1.112', username='ahmad', password='toor')
            self.pihole.setStyleSheet("background-color : green")
            # self.client.close()

            self.clientUnms.connect(
                '192.168.1.185', username='ahmad', password='toor')
            self.unms.setStyleSheet("background-color : green")
            # self.client.close()

            self.clientClouds.connect(
                '192.168.1.183', username='ahmad', password='toor')
            self.clouds.setStyleSheet("background-color : green")
            # self.client.close()
        except Exception as er:
            print(er)

    def shutdownClouds(self):
        try:
            transport = self.clientClouds.get_transport()
            session = transport.open_session()
            session.set_combine_stderr(True)
            session.get_pty()
            session.exec_command(self.command)
            stdin = session.makefile('wb', -1)
            stdout = session.makefile('rb', -1)
            stdin.write("toor"+'\n')
            stdin.flush()

        except Exception as er:
            print(er)

    def shutdownPihole(self):
        try:
            transport = self.clientPihole.get_transport()
            session = transport.open_session()
            session.set_combine_stderr(True)
            session.get_pty()
            session.exec_command(self.command)
            stdin = session.makefile('wb', -1)
            stdout = session.makefile('rb', -1)
            stdin.write("toor"+'\n')
            stdin.flush()

            print(stdout.read().decode())
            self.unms.setStyleSheet("background-color : red")
        except Exception as er:
            print(er)

    def shutdownUnms(self):
        try:
            # stdin, stdout, stderr = self.clientUnms.exec_command(
            #     self.command)
            transport = self.clientUnms.get_transport()
            session = transport.open_session()
            session.set_combine_stderr(True)
            session.get_pty()
            session.exec_command(self.command)
            stdin = session.makefile('wb', -1)
            stdout = session.makefile('rb', -1)
            stdin.write("toor"+'\n')
            stdin.flush()

            print(stdout.read().decode())
            self.unms.setStyleSheet("background-color : red")

        except Exception as er:
            print(er)

            # commands = [
            #     "pwd",
            #     "id",
            #     "sudo apt-get update",
            #     "df -h"
            # ]

            # for command in commands:
            #     print("="*50, command, "="*50)
            #     stdin, stdout, stderr = client.exec_command(command)
            #     print(stdout.read().decode())
            #     err = stderr.read().decode()
            #     if err:
            #         print(err)


            # client.close()
app = QtWidgets.QApplication([])
win = control_server()
win.show()
sys.exit(app.exec())
