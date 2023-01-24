import sys
import os
import socket
from core import *
from utils import loadJson, dumpJson, popUp, decrypt
from PyQt5.QtWidgets import QMainWindow, QPushButton, QLineEdit, QApplication, QWidget, QLabel, QListWidget
from PyQt5 import uic


ip = "localhost"
port = 1034


class Client:
    _buffer_size = 1024
    path = ""

    def __init__(self, ip=ip, port=port, key=key) -> None:
        self.ip = ip
        self.port = port
        self.key = key

        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(yellow + f"Connection to: {ip}:{port}")
        self.socket.connect((self.ip, self.port))

    def changePath(self, newPath: str):
        self.path = newPath
        return self.path

    def sendCredentials(self, service: str, password: str):
        self.socket.send(dumpJson(
            {"path": self.path, "key": self.key, "pwd": password, "service": service}, encoding))

        print(green + "Sent credentials")

        if not loadJson(self.socket.recv(self._buffer_size), encoding)["code"] == 201:
            return 1

        print(blue + "Recived response")

        return 0

    def getAll(self):
        self.socket.send(dumpJson(
            {"path": self.path, "key": self.key}, encoding))

        return loadJson(self.socket.recv(self._buffer_size), encoding)["all"]

    def getElements(self, service: str):
        self.socket.send(dumpJson(
            {"path": self.path, "key": self.key, "service": service}, encoding))

        return loadJson(self.socket.recv(self._buffer_size), encoding)["all"]


class Manage(QWidget):
    def __init__(self) -> None:
        super(Manage, self).__init__()

        # loading Add ui
        uic.loadUi(r"./app/UI/manage.ui", self)

        # setting
        self.setWindowTitle("Manage pwds")
        self.setFixedHeight(203)
        self.setFixedWidth(250)

        # get components
        self.add = self.findChild(QPushButton, "AddButton")
        self.delete = self.findChild(QPushButton, "DeleteButton")
        self.service = self.findChild(QLineEdit, "ServiceLine")
        self.password = self.findChild(QLineEdit, "PasswordLine")

        self.add.clicked.connect(self.AddPushed)
        self.delete.clicked.connect(self.DeletePushed)

    def AddPushed(self):
        client.changePath("add")

        if not client.sendCredentials(self.service.text(), self.password.text()) == 0:
            return popUp("Error", f"password - {self.password.text()} not added")

        popUp("Success", f"password - {self.password.text()} added")

    def DeletePushed(self):
        client.changePath("delete")

        if not client.sendCredentials(self.service, self.password) == 0:
            popUp("Error", f"password - {self.password} not deleted")

        popUp("Success", f"password - {self.password} deleted")


class Search(QWidget):
    def __init__(self) -> None:
        super().__init__()

        # loading Search ui
        uic.loadUi(r"./app/UI/search.ui", self)

        # setting
        self.setWindowTitle("Search your passwords")
        self.setFixedHeight(300)
        self.setFixedWidth(400)

        # get elements
        self.search = self.findChild(QPushButton, "SearchButton")
        self.service = self.findChild(QLineEdit, "ServiceLine")
        self.pwds = self.findChild(QListWidget, "PasswordList")

        self.search.clicked.connect(self.SendPushed)

    def SendPushed(self):
        if self.service.text() == "":
            client.changePath("all")

            for object_ in client.getAll():
                self.pwds.addItem(
                    f"{object_['service']} : {decrypt(object_['pwd'])}\n")
        else:
            client.changePath("element")
            
            self.pwds.clear()

            for object_ in client.getElements(self.service.text()):
                self.pwds.addItem(f"{decrypt(object_['pwd'])}\n")


class Window(QMainWindow):
    def __init__(self) -> None:
        super(Window, self).__init__()

        # loading main ui
        uic.loadUi(r"./app/Ui/main.ui", self)

        # setting
        self.setWindowTitle("PWD")
        self.setFixedHeight(119)
        self.setFixedWidth(226)

        # get buttons
        self.manage = self.findChild(QPushButton, "ManageButton")
        self.search = self.findChild(QPushButton, "SearchButton")

        self.manage.clicked.connect(self.ManagePushed)
        self.search.clicked.connect(self.searchPushed)

        self.show()

    def ManagePushed(self):
        manage.show()

    def searchPushed(self):
        search.show()


if __name__ == "__main__":
    os.system('')

    app = QApplication(sys.argv)
    search = Search()
    manage = Manage()
    Ui = Window()
    client = Client(ip=ip, port=port, key=key)

    app.exec()
