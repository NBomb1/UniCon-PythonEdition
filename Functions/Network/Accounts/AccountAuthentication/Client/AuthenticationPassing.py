import hashlib
import socket as s
from ast import literal_eval

from Functions.Network.Accounts.AccountData import Account
from Functions.Network.Accounts.AccountDataManager import AccountManager
from Functions.Network.DataTransfer import MessageTransfer
from Functions.Network.Info import Info
from Functions.Tools.logManager import Logs
from Functions.Exceptions.Authentication import Client


class Authentication:
    def __init__(self, messageTransfer: MessageTransfer, logs: Logs, password: str, askPassword: callable,
                 account: AccountManager):
        self.messageTransfer = messageTransfer
        self.socket = messageTransfer.socket
        self.logs = logs
        self.password = password
        self.askPassword = askPassword
        self.account = account

    def start(self):
        try:
            # Phase 1
            self._1_PhaseRecognition()
            self.checkPhasePassing()

            # Phase 2
            self._2_PhaseBuiltInModuleCheck()
            self.checkPhasePassing()

            # Phase 3
            self._3_PhasePasswordCheck()

            self._4_PhaseDataShare()
            # Phase 5 is not available now
            # Phase 6 is not available now
            self.logs.sendLog('[Authentication Client] Connection established!', -1)
            self.messageTransfer.handleMessages()
        except Client.PhaseFailedException as fail:
            self.logs.sendLog(f"[Authentication Client] Couldn't pass authentication phase. Reason: {fail}", -1)
            raise fail

    def sendMessage(self, message: str, count: int) -> int:
        # decoded non-english symbols can take more than 1 length of message
        return self.socket.send((message + (" " * (count - len(message.encode())))).encode())

    def _getMessage(self, length=Info.preAuthMessageLength) -> str | None:
        try:
            message = self.socket.recv(length)
            return message.decode()  # getting special message
        except s.timeout:
            return None
        except ConnectionAbortedError:
            return None
        except OSError:
            return None

    def _1_PhaseRecognition(self):
        self.logs.sendLog("[Authentication Client] Trying to pass 1st phase.", -1)
        self.sendMessage(Info.unique_message, Info.preAuthMessageLength)

    def _2_PhaseBuiltInModuleCheck(self):
        self.logs.sendLog("[Authentication Client] Trying to pass 2nd phase.", -1)
        self.sendMessage(Info.getBuiltInModules().__str__(), Info.preAuthMessageLength)

    def _3_PhasePasswordCheck(self):
        self.logs.sendLog("[Authentication Client] Trying to pass 3rd phase.", -1)
        salt = self.socket.recv(Info.preAuthMessageLength)  # receiving salt
        self.account.getSelfAccount().setSalt(salt)

        hashed_password = hashlib.sha512(salt + self.password.encode()).hexdigest()
        self.socket.send(hashed_password.encode())

        while (message := self._getMessage()) is not None and not bool(message.replace(' ', '')):
            try:
                self.socket.send(hashlib.sha512(salt + (self.askPassword()).encode()).hexdigest().encode())
            except TypeError:
                self.socket.close()
                self.logs.sendLog("[Authentication Client] Connection closed.", -1)

    def _4_PhaseDataShare(self):
        # sending nickname and pc name
        nickname = self.account.getSelfAccount().nickname
        pc_name = self.account.getSelfAccount().pc_name
        self.sendMessage(nickname, Info.preAuthMessageLength)
        self.sendMessage(pc_name, Info.preAuthMessageLength)

        # Getting id
        id = self._getMessage().rstrip(' ')
        self.account.getSelfAccount().setId(id)

        try:
            accounts: list[dict[str:str]] = literal_eval(self._getMessage(Info.preAuthGetAccountInfo).rstrip(' '))
            for i in accounts:
                self.logs.sendLog(f"[Authentication Client] Adding {i['nickname']} with {i['tags']}", -1)
                account = Account(

                    # creating a new MessageTransfer if it is not owner
                    MessageTransfer(self.messageTransfer.accountManager, None)
                    if 'Owner' not in i['tags']
                    else self.messageTransfer,

                    self.messageTransfer.socket.getpeername()[0],
                    self.messageTransfer.socket.getpeername()[1],
                    i['nickname'],
                    i['pc_name'],
                    i['id'],
                    None,
                    i['tags']
                )
                self.account.add(account)
                if 'Owner' in i['tags']:
                    self.account.owner = account
            self.messageTransfer.registerAccount(self.account.owner)
        except ValueError:
            self.logs.sendLog('[Authentication Client] Something went wrong due getting an account info.', -1)
            self.socket.close()

        # self.checkPhasePassing()

    def checkPhasePassing(self):
        text = self._getMessage().rstrip(' ')
        if text != 'pass':
            raise Client.PhaseFailedException(text)
