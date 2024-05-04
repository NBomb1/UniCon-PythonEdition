import socket
import threading
from ast import literal_eval
from time import sleep

from Functions.Exceptions.DataTransfer import DataTransfer

"""Is not done yet."""


class MessageTransfer:
    types = []
    registeredFunctions: dict[str, list[callable]] = {}
    account = None
    sendMessages: list[bytes] = []

    def __init__(self, accountManager, s: socket.socket):
        self.accountManager = accountManager
        self.socket = s
        self.registerType('ModuleConnector')
        self.senderHandler()

    def registerType(self, type_: str):
        if type_ not in self.types:
            self.types.append(type_)

    def registerFunction(self, type_: str, func: callable):
        if self.registeredFunctions.get(type_) is None:
            self.registeredFunctions[type_] = [func]
        else:
            self.registeredFunctions[type_].append(func)

    def send_message(self, type_: str, **kwargs):
        if type_ not in self.types:
            raise DataTransfer.TypeDoesntExistError(f"Type {type_} doesn't exists.")
        kwargs['type'] = type_
        message = len(kwargs.__str__()).__str__() + kwargs.__str__()

        self.sendMessages.append(message.encode())
        # self.socket.send(message.encode())

    def _receiveMessage(self):
        length = ''
        while True:
            got = self.socket.recv(1).decode()
            if got == '{':
                length = int(length)
                break
            else:
                length = length + got
        message = '{' + self.socket.recv(length - 1).decode()
        print(length, message)
        assert message[-1] == '}'
        return message

    def handleMessages(self):
        def handler():
            while True:
                message = self._receiveMessage()
                message = literal_eval(message)
                assert message['type'] is not None
                message['_socket'] = self.socket
                message['_account'] = self.account
                for func in self.registeredFunctions.get(message['type']):
                    func(message)

        self.account = self.accountManager.findBySocket(self.socket)
        assert self.account is not None
        threading.Thread(target=handler, daemon=True).start()

    def senderHandler(self):
        def handler():
            while True:
                for i in self.sendMessages:
                    self.socket.send(i)
                    self.sendMessages.remove(i)
                sleep(0.001)

        threading.Thread(target=handler, daemon=True).start()
