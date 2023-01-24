import socket
import datetime
import argparse
from core import *
from utils import loadJson, dumpJson, encrypt


funcions = {}

args = argparse.ArgumentParser()
args.add_argument("--host", type=str, help="Host server", default="localhost")
args.add_argument("--port", type=int, help="Port server", default=1034)
args.add_argument("--bf", type=int, help="Buffer size", default=1024)

parse = args.parse_args()


def packet(parms):
    def wrapper(func):
        funcions[parms] = func

        return func
    return wrapper


@packet("add")
def addToDB(pwd: str, service: str):
    if not db.addPassword(encrypt(pwd), service) == 0:
        return dumpJson({"code": 401}, encoding)

    return dumpJson({"code": 201}, encoding)


@packet("delete")
def deleteToDB(pwd: bytes, service: str):
    if not db.deletePassword(encrypt(pwd), service) == 0:
        return dumpJson({"code": 402}, encoding)

    return dumpJson({"code": 202}, encoding)


def createLog(file: str, data: str) -> int:
    try:
        fileLog = open(file, "a")
        fileLog.write(f"{datetime.datetime.now()} {data}")
        fileLog.close()

        return True
    except Exception as e:
        print(e)


class Server():
    __socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    __socket.bind((parse.host, parse.port))
    __socket.listen(1)

    print(green + f"Server online: {white}{parse.host}:{parse.port}" + reset)

    def connection(self):
        while True:
            connection, add = self.__socket.accept()
            self.head(connection, add)

    def head(self, connection, add):
        try:
            while True:
                print(blue + F"{add[0]}:{add[1]}" + reset)

                if not createLog(r"./logs/connection.log", f"Connection log: {add[0]}\n"):
                    print(red + "Impossible save this log!" + reset)

                recv = loadJson(connection.recv(parse.bf), encoding)
                path = recv["path"]

                if not recv["key"] == key:
                    connection.send(
                        dumpJson({"status": "invalid key or key not found"}))

                if path == "add":
                    print(blue + f"Adding password: {recv['pwd']}")
                    connection.send(funcions["add"](
                        recv["pwd"], recv["service"]))

                elif path == "delete":
                    print(blue + f"Deleting password: {recv['pwd']}")
                    connection.send(funcions["delete"](
                        recv["pwd"], recv["service"]))

                elif path == "all":
                    print(blue + "Sending data - all")
                    connection.send(dumpJson({"all": db.getAll()}, encoding))

                elif path == "element":
                    print(blue + f"Sending data - {recv['service']}")
                    if elements := db.searchSingleElement(recv["service"]):
                        connection.send(dumpJson({"all": elements}, encoding))

                else:
                    # unused status
                    connection.send(
                        dumpJson({"status": 1}, encoding))
        except:
            pass


if __name__ == "__main__":
    server = Server()
    server.connection()
