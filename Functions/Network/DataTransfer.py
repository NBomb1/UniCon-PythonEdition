import socket
import threading
import traceback
from traceback import format_exc
from ast import literal_eval
from time import sleep

from Functions.Exceptions.DataTransfer import DataTransfer
from typing import TYPE_CHECKING

from Functions.Network.FileTransfer.Data.Actions import Actions
from Functions.Network.FileTransfer.Data.States import RequestStates

if TYPE_CHECKING:
    from Functions.Network.Accounts.AccountData import Account
    from Functions.Network.Accounts.AccountManager import AccountManager


class MessageTransfer:

    def __init__(self,
                 accountManager: 'AccountManager',
                 s: socket.socket | None,
                 errorFunction=None,
                 description: str | None = None
                 ):
        self.registeredFunctions: dict[str, list[callable]] = {}
        self.account = None  # the problem is right here
        self.accountManager = accountManager
        self.logs = accountManager.logs
        self.socket = s
        self.sendMessages: list[bytes] = []
        self.errorFunction: callable = errorFunction
        self.description = description

    def registerAccount(self, account: 'Account'):
        self.account = account

    def registerType(self, type_: str):
        if self.registeredFunctions.get(type_) is None:
            self.registeredFunctions[type_] = []

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
        except Exception as error:
            self._callErrorFunc(error)
            return False

    def send_message(self, type_: str, thread=True, **kwargs) -> None | bool:
        assert self.socket is not None, \
            "The socket is None. You can't send anything if socket is not registered."

        if self.registeredFunctions.get(type_) is None:
            raise DataTransfer.TypeDoesntExistError(f"Type {type_} doesn't exists.",
                                                    self.registeredFunctions)
        kwargs['type'] = type_
        message = len(kwargs.__str__().encode()).__str__() + kwargs.__str__()

        if type_ == 'FileTransfer':
            kwargs['action'] = Actions.actions_dict_int_to_str.get(kwargs['action'])
            kwargs['state'] = RequestStates.states_dict_int_to_str.get(kwargs['state'])
            print(f"Sending: {kwargs}")  # TODO: DELETE IT
            kwargs['action'] = Actions.actions_dict_str_to_int.get(kwargs['action'])
            kwargs['state'] = RequestStates.states_dict_str_to_int.get(kwargs['state'])
        if thread:
            self.sendMessages.append(message.encode())
        else:
            return self._send(message.encode())

    def _receiveMessage(self):
        """
        Basically, recv() will make thread wait until it will get any data.
        If the data is empty, it means that buffer is empty and socket is shut down.
        So it will just close it after all messages will be handled.
        """
        length = ''
        while True:
            got = self.socket.recv(1).decode()
            if got == '{':
                length = int(length)
                break
            elif got == '':
                self.socket.close()
            else:
                length = length + got
        message = '{' + self.socket.recv(length - 1).decode()
        assert message[-1] == '}', "An error occurred while getting message."
        return message

    def handleMessages(self):
        assert self.socket is not None, \
            "The socket is None. You can't send anything if socket is not registered."

        def message_handler():
            try:
                while True:
                    message = self._receiveMessage()
                    message = literal_eval(message)

                    assert message['type'] is not None, 'Type cant be None'
                    assert self.registeredFunctions.get(message['type']) is not None, \
                        f"""Type "{message["type"]}" is not in list: {tuple(self.registeredFunctions.values())}. """ + \
                        f"""{self.description}"""

                    if (funcList := self.registeredFunctions.get(message['type'])) is None:
                        self.logs.sendLog(f'No functions were registered for type {message["type"]}', -1)
                        return
                    message['_socket'] = self.socket
                    message['_account'] = self.account
                    if message['type'] == 'close':  # recheck it
                        print('reg Functions', self.registeredFunctions)
                    elif message['type'] == 'FileTransfer':  # TODO: DELETE IT
                        self.logs.sendLog(f'got: {message}, {funcList}', -2)
                    for func in funcList:
                        func(message)
            except Exception as error:
                self.logs.sendLog(f'[MessageTransfer] An error occurred while handling message error: {error}', -1)
                self.logs.sendLog(f'[MessageTransfer] Details: {traceback.format_exc()}', -1)
                self._callErrorFunc(error)
        threading.Thread(target=message_handler, daemon=True).start()

    def senderHandler(self):
        assert self.socket is not None, \
            "The socket is None. You can't send anything if socket is not registered."

        def sender_handler():
            while True:
                try:
                    for i in self.sendMessages:
                        self.logs.sendLog(i.decode(), -2)
                        self._send(i)
                        self.sendMessages.remove(i)
                except Exception as error:
                    self.logs.sendLog(f"[MessageTransfer] An error occurred while sending message error: {error}", -1)
                    print(format_exc())
                    print('ERROR! - \n', error, '\ninfo: ', i, '\nlist: ', self.sendMessages)
                    self._callErrorFunc(error)
                sleep(0.001)
        threading.Thread(target=sender_handler, daemon=True).start()

    def registerErrorFunction(self, func: callable):
        """Sets the function when the error occurs."""
        self.errorFunction = func

    def _callErrorFunc(self, error: Exception):
        if self.errorFunction is not None:
            self.errorFunction(error, self)
