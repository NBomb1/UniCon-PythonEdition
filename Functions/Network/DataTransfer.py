import socket
import threading
from traceback import format_exc
from ast import literal_eval
from time import sleep

from Functions.Exceptions.DataTransfer import DataTransfer
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Functions.Network.Accounts.AccountData import Account

"""Is not done yet."""


class MessageTransfer:

    def __init__(self, accountManager, s: socket.socket | None):
        self.types = []
        self.registeredFunctions: dict[str, list[callable]] = {}
        self.account = None  # the problem is right here
        self.accountManager = accountManager
        self.logs = accountManager.logs
        self.socket = s
        self.sendMessages: list[bytes] = []
        self.errorFunction: callable = None

    def registerAccount(self, account: 'Account'):
        self.account = account

    def registerType(self, type_: str):
        if type_ not in self.types:
            self.types.append(type_)

    def registerFunction(self, type_: str, func: callable):
        """This will return to registered function a dictionary with all the data in message"""
        if self.registeredFunctions.get(type_) is None:
            self.registeredFunctions[type_] = [func]
        else:
            self.registeredFunctions[type_].append(func)

    def _send(self, text: bytes) -> bool:
        """Returns true if message was sent successfully"""
        try:
            self.socket.send(text)
            return True
        # except ConnectionResetError as error:  # client disconnected
        #     self._callErrorFunc(error)
        #     return False
        # except OSError as error:  # client was disconnected in code, but code didn't stop
        #     self._callErrorFunc(error)
        #     return False
        except Exception as error:
            self._callErrorFunc(error)
            return False

    def send_message(self, type_: str, thread=True, **kwargs) -> None | bool:
        assert self.socket is not None, \
            "The socket is None. You can't send anything if socket is not registered."

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
        assert message[-1] == '}'
        return message

    def handleMessages(self):
        assert self.socket is not None, \
            "The socket is None. You can't send anything if socket is not registered."

        def handler():
            try:
                while True:
                    message = self._receiveMessage()
                    message = literal_eval(message)

                    assert message['type'] is not None, 'Type cant be None'
                    assert message['type'] in self.types, f"""Type "{message["type"]}" is not in list: {self.types}"""

                    if (funcList := self.registeredFunctions.get(message['type'])) is None:
                        print(f'No functions were registered for type {message["type"]}')
                        return
                    message['_socket'] = self.socket
                    message['_account'] = self.account
                    # print('output:', message)
                    for func in funcList:
                        func(message)
            # except ConnectionResetError:
            #     pass  # needs to be done
            except Exception as error:
                self._callErrorFunc(error)
        threading.Thread(target=handler, daemon=True).start()

    def senderHandler(self):
        assert self.socket is not None, \
            "The socket is None. You can't send anything if socket is not registered."

        def handler():
            while True:
                try:
                    for i in self.sendMessages:
                        self.logs.sendLog(i.decode(), -2)
                        self._send(i)
                        self.sendMessages.remove(i)
                except Exception as error:
                    print('ERROR! - \n', error, '\ninfo: ', i, '\nlist: ', self.sendMessages)
                    print(format_exc())
                    self._callErrorFunc(error)
                sleep(0.001)
        threading.Thread(target=handler, daemon=True).start()

    def registerErrorFunction(self, func: callable):
        self.errorFunction = func

    def _callErrorFunc(self, error: Exception):
        if self.errorFunction is not None:
            self.errorFunction(error)
