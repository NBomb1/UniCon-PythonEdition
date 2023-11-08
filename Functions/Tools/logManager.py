import io
from os import getcwd, makedirs
from datetime import datetime
from inspect import getsourcefile

import _tkinter


class Logs:
    registeredFunctions: dict[int: list[callable]] = {}  # contains id log and functions
    registeredFileLog: dict[int: io.FileIO] = {}
    ver = "0.0.1"

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

    def sendLog(self, message: str, id_: int):
        for i in self.registeredFunctions[id_]:
            i(message, id_)
        if self.registeredFileLog.get(id_) is not None:
            self.registeredFileLog[id_].write(f"[{datetime.now().__str__()}]: " + message + "\n")

    def registerFileLog(self, id_):
        if self.registeredFunctions.get(id_) is None:
            raise ValueError("There is no registered id (" + str(id_) + ").")

        if self.registeredFileLog.get(id_) is None:
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

    def closeFiles(self):
        for i in self.registeredFileLog.values():
            try:
                self.sendLog(f'[LogManager] File ({i.name.replace(getcwd(), "")}) is closing.', 0)
            except _tkinter.TclError:
                pass

            i.write(f"[{datetime.now().__str__()}]: [LogManager] File is closing. \n")
            i.close()
