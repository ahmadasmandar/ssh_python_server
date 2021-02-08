from PyQt5 import QtWidgets, uic, QtSerialPort, QtCore, QtGui, QtWidgets
import os
import sys
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtWidgets import QMessageBox, QSlider

import paramiko
from paramiko import SSHClient
import traceback
import signal

enter_key = "\n"


class control_server(QtWidgets.QMainWindow):
    def __init__(self):
        super(control_server, self).__init__()
        uic.loadUi("mainwindow.ui", self)
        self.clouds.clicked.connect(self.shutdownClouds)
        self.pihole.clicked.connect(self.shutdownPihole)
        self.unms.clicked.connect(self.shutdownUnms)
        self.reserve.clicked.connect(self.exit_function)

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
            self.clientPihole.connect("192.168.1.112", username="ahmad", password="toor")
            self.pihole.setStyleSheet("background-color : #66bb6a")
            # self.client.close()

            self.clientUnms.connect("192.168.1.185", username="ahmad", password="toor")
            self.unms.setStyleSheet("background-color : #66bb6a")
            # self.client.close()

            self.clientClouds.connect("192.168.1.183", username="ahmad", password="toor")
            self.clouds.setStyleSheet("background-color : #66bb6a")
            # self.client.close()
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("*** Exception:")
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)

    def shutdownClouds(self):
        try:

            transport = self.clientClouds.get_transport()
            session = transport.open_session()
            session.set_combine_stderr(True)
            session.get_pty()
            session.exec_command(self.command)
            stdin = session.makefile("wb", -1)
            stdout = session.makefile("rb", -1)
            stdin.write("toor" + "\n")
            stdin.flush()

        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("*** Exception:")
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)

    def shutdownPihole(self):
        try:
            transport = self.clientPihole.get_transport()
            session = transport.open_session()
            session.set_combine_stderr(True)
            session.get_pty()
            session.exec_command(self.command)
            stdin = session.makefile("wb", -1)
            stdout = session.makefile("rb", -1)
            stdin.write("toor" + "\n")
            stdin.flush()

            print(stdout.read().decode())
            self.unms.setStyleSheet("background-color : red")
        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("*** Exception:")
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)

    def shutdownUnms(self):
        try:
            # stdin, stdout, stderr = self.clientUnms.exec_command(
            #     self.command)
            transport = self.clientUnms.get_transport()
            session = transport.open_session()
            session.set_combine_stderr(True)
            session.get_pty()
            session.exec_command("sudo apt-get update")
            stdin = session.makefile("wb", -1)
            stdout = session.makefile("rb", -1)
            stdin.write("toor" + "\n")
            stdin.flush()

            print(stdout.read().decode())
            self.unms.setStyleSheet("background-color : #ec407a")
            self.unms.setDisabled(True)

        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("*** Exception:")
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
            # print("*** print_exception:")
            # # exc_type below is ignored on 3.5 and later
            # traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
            # print("*** Error Linenumber:", exc_traceback.tb_lineno)

    def sendSudoCommand(self, command, client):
        try:
            # stdin, stdout, stderr = self.clientUnms.exec_command(
            #     self.command)
            transport = client.get_transport()
            session = transport.open_session()
            session.set_combine_stderr(True)
            session.get_pty()
            session.exec_command(command)
            stdin = session.makefile("wb", -1)
            stdout = session.makefile("rb", -1)
            stdin.write("toor" + "\n")
            stdin.flush()
            message = stdout.read().decode()
            # print(message)

            return message.replace("toor", " ").replace("[sudo] password for ahmad:", " ").strip()

        except Exception:
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print("*** Exception:")
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
            # print("*** print_exception:")
            # # exc_type below is ignored on 3.5 and later
            # traceback.print_exception(exc_type, exc_value, exc_traceback, limit=2, file=sys.stdout)
            # print("*** Error Linenumber:", exc_traceback.tb_lineno)

    def exit_function(self):
        # self.message_6 = QMessageBox.question(
        #     self, "  EXIT Confirm", "Do you want to EXIT ?  ", QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        # )

        # if self.message_6 == QMessageBox.Yes:
        #     exit()

        msg = QMessageBox()
        msg.setStyleSheet(
            "QLabel{min-width:200 px;height: 200px; ;font-size: 12px;}QPushButton{ width:60px; font-size: 10px; }QTextEdit{background: white;border-radius: 5px;border: 2px solid #1e88e5;height: 200px;}"
        )

        msg.setWindowTitle("Hallo Ahmad")
        msg.setText("This is the main text!")
        msg.setIcon(QMessageBox.Question)
        msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Retry | QMessageBox.Ignore)
        msg.setDefaultButton(QMessageBox.Retry)
        msg.setInformativeText("informative text, ya!")
        msg.buttonClicked.connect(self.popup_button)

        self.read_out = self.sendSudoCommand("sudo apt-get update", self.clientUnms)
        msg.setDetailedText(str(self.read_out).strip())
        msg.exec_()

    def popup_button(self):
        # print("hallo mensch")
        print(str(self.read_out))


app = QtWidgets.QApplication([])
win = control_server()
win.show()
sys.exit(app.exec())
