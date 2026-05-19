import socket
import threading

from Functions.Network.Accounts.AccountManager import AccountManager
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
                socket = MessageTransfer(self.accountManager, s, description=f"Module: {i.moduleId}")
                socket.account = i.account
                i.setMessageTransfer(socket)
                i.func(i)
                self.__waitingForConnections.remove(i)
                i.account.addExtraConnection(i.moduleId, i.socket)
                self.accountManager.getSelfAccount().addExtraConnection(i.moduleId, i.socket)
                self.accountManager.logs.sendLog(
                    f"[MCM Server] Module "
                    f"{i.moduleId[:3]}...{i.moduleId[-3:]} "
                    f"established extra connection to client {i.account.id}.", -1
                )
                return True
        return False

    def _deleteCheckCode(self, obj: WaitingForConnectionInfo):
        try:
            self.__waitingForConnections.remove(obj)
            self.accountManager.logs.sendLog(
                f"[MCM Server] Module "
                f"{obj.moduleId[:3]}...{obj.moduleId[-3:]}"
                f"connection to client {obj.account.id} timed out.", -1
            )
            obj.declined()
        except ValueError:
            pass
