import socket
import threading

from Functions.Network.Accounts.AccountDataManager import AccountManager
from Functions.Network.DataTransfer import MessageTransfer
from Functions.Network.ModuleConnector.WaitingForConnectionInfo import WaitingForConnectionInfo


class ModuleConnectorManager:
    def __init__(self, accountManager: AccountManager):
        self.__waitingForConnections: list[WaitingForConnectionInfo] = []
        self.accountManager = accountManager

    def addConnectionWaiting(self, obj: WaitingForConnectionInfo):
        self.__waitingForConnections.append(obj)
        threading.Timer(obj.timeout, self._deleteCheckCode, args=(obj, )).start()

    def checkSpecialCode(self, specialCode: str, s: socket.socket):
        for i in self.__waitingForConnections:
            if i.specialCode.decode() == specialCode:
                i.setMessageTransfer(MessageTransfer(self.accountManager, s))
                i.func(i)
                self.__waitingForConnections.remove(i)
                i.account.addExtraConnection(i.moduleId, i.socket)
                return True
        return False

    def _deleteCheckCode(self, obj: WaitingForConnectionInfo):
        try:
            self.__waitingForConnections.remove(obj)
        except ValueError:
            pass

