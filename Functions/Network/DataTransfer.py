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
        self.logs = accountManager.logs
        self.socket = s

    def registerType(self, type_: str):
        if type_ not in self.types:
            self.types.append(type_)

    def registerFunction(self, type_: str, func: callable):
        if self.registeredFunctions.get(type_) is None:
            self.registeredFunctions[type_] = [func]
        else:
            self.registeredFunctions[type_].append(func)

    def _send(self, text: bytes) -> bool:
        """Returns true if message was sent successfully"""
        try:
            self.socket.send(text)
            return True
        except ConnectionResetError:  # client disconnected
            return False
        except OSError:  # client was disconnected in code, but code didn't stop
            return False

    def send_message(self, type_: str, thread=True, **kwargs) -> None | bool:
        if type_ not in self.types:
            raise DataTransfer.TypeDoesntExistError(f"Type {type_} doesn't exists.")
        kwargs['type'] = type_
        message = len(kwargs.__str__()).__str__() + kwargs.__str__()

        if thread:
            self.sendMessages.append(message.encode())
        else:
            return self._send(message.encode())

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
                assert message['type'] in self.types
                if (funcList := self.registeredFunctions.get(message['type'])) is None:
                    print(f'No functions were registered for type {message["type"]}')
                    return
                message['_socket'] = self.socket
                message['_account'] = self.account
                for func in funcList:
                    func(message)

        self.account = self.accountManager.findBySocket(self.socket)
        assert self.account is not None
        threading.Thread(target=handler, daemon=True).start()

    def senderHandler(self):
        def handler():
            while True:
                for i in self.sendMessages:
                    print('before sending:', i, '\n', self.sendMessages)
                    self.logs.sendLog(i.decode(), -2)
                    self._send(i)
                    print(self.sendMessages)
                    self.sendMessages.remove(i)
                sleep(0.001)

        threading.Thread(target=handler, daemon=True).start()
