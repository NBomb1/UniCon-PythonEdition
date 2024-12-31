import io
import threading
from functools import partial
from os import getcwd, makedirs
from datetime import datetime
from inspect import getsourcefile
from time import sleep

import _tkinter

import settings


class Logs:
    registeredFunctions: dict[int: list[callable]] = {}  # contains id log and functions
    registeredFileLog: dict[int: io.FileIO] = {}
    logsMessages: list[callable] = []
    ver = "1.0.2"

    def __init__(self):
        self.printFlag = False
        self.functionWaiterFlag = False
        self.handler()

    def registerId(self, id_, ignoreRegistered=False):
        if self.registeredFunctions.get(id_) is None:
            self.registeredFunctions[id_] = []
            self.sendLog(f'[LogManager] Log with id {id_} has been registered.', 0)
        else:
            if not ignoreRegistered:
                self.sendLog(f"[LogManager] Log with id {id_} has already been registered!", 0)

    def registerHandler(self, id_: int, function: callable):
        self.registerId(id_, True)
        self.registeredFunctions[id_].append(function)
        self.sendLog(
                     f'[LogManager] Function ({function.__name__}) '
                     f'from ({getsourcefile(function).replace(getcwd(), "")}) has been registered - id: {id_}.',
                     0)

    def _sendLog(self, message: str, id_: int, time: datetime):
        if self.functionWaiterFlag and not self.registeredFunctions[id_]:
            self.logsMessages.insert(0, partial(self._sendLog, message, id_, time))
            return
        for i in self.registeredFunctions[id_]:
            i(message, id_, time)
        if self.registeredFileLog.get(id_) is not None:
            self.registeredFileLog[id_].write(f"[{time.__str__()}]: " + message + "\n")
        if id_ == 'All ids' and self.printFlag:
            print(f"[{time.__str__()}]: " + message)

    def sendLog(self, message: str, id_: int):
        self.logsMessages.append(partial(self._sendLog, message, id_, datetime.now()))
        self.logsMessages.append(partial(self._sendLog, f"{id_} " + message, 'All ids', datetime.now()))

    def sendAll(self, message: str):
        for i in self.registeredFunctions.keys():
            self.logsMessages.append(partial(self._sendLog, message, i, datetime.now()))

    def handler(self):
        def cycle():
            while True:
                try:
                    # '' if not self.logsMessages else print(self.logsMessages)
                    if self.logsMessages:
                        self.logsMessages.pop(0)()
                    sleep(settings.LogManager.messageDelay)
                except ValueError:  # I/O operation on closed file
                    pass

        threading.Thread(target=cycle, daemon=True).start()

    def registerFileLog(self, id_, force=False):
        print("Registering file log for id " + str(id_) + "...")
        if self.registeredFunctions.get(id_) is None and not force:
            raise ValueError("There is no registered id (" + str(id_) + ").")

        if self.registeredFileLog.get(id_) is None:
            self.registerId(id_, True)
            path = getcwd() + "\\Logs\\"
            time = datetime.now().__str__().replace(":", "-")
            result = path + time + " id - " + str(id_) + ".txt"

            makedirs(path, exist_ok=True)
            self.registeredFileLog[id_] = open(
                result,
                mode="w+",
                encoding="utf-8"
            )
            self.sendLog(f'[LogManager] File log ({result.replace(getcwd(), "")}) has been registered.', 0)
            self.registeredFileLog[id_].write(
                f"[{datetime.now().__str__()}]: [LogManager] Log file has been created. \n"
            )
        print("Registering of file log for id " + str(id_) + " completed.")

    def closeFiles(self):
        for i in self.registeredFileLog.values():
            try:
                self.sendLog(f'[LogManager] File ({i.name.replace(getcwd(), "")}) is closing.', 0)
            except _tkinter.TclError:
                pass

            i.write(f"[{datetime.now().__str__()}]: [LogManager] File is closing. \n")
            i.close()

    def showLogs(self):
        self.printFlag = True

    def enableFunctionWaiter(self):
        self.functionWaiterFlag = True
