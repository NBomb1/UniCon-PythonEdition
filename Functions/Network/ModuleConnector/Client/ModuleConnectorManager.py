import hashlib
import socket
from functools import partial

from Functions.ModuleHandler.moduleLoader import ModuleLoader
from Functions.Network.Accounts.AccountData import Account
from Functions.Network.Accounts.AccountDataManager import AccountManager
from Functions.Network.DataTransfer import MessageTransfer
from Functions.Network.ModuleConnector.Client.InviteConnectionInfo import InviteConnectionInfo


class ClientModuleConnectorManager:
    def __init__(self, s: MessageTransfer, moduleHandler: ModuleLoader, accountManager: AccountManager):
        self.moduleHandler = moduleHandler
        self.messageTransfer = s
        self.accountManager = accountManager
        self.messageTransfer.registerFunction('ModuleConnector', self.getInvite)
        self.salt = s.accountManager.getSelfAccount().salt

    def getInvite(self, message: dict):
        # dict['type', 'id', 'specialCode', 'socket']

        for module in self.moduleHandler.active:
            if module.id_ == message['id'] and module.defaultNetworkAuth:
                module.object.mcm_inviteConnection(InviteConnectionInfo(
                    message['specialCode'],
                    message['_account'],
                    message['id'],  # the id of module
                    None,  # the version will be None for a while,
                    partial(self.__accept, message['specialCode'], message['id'], message['_account'], message['id'])
                ))

    def __accept(self, specialCode: bytes, id_: str, account: Account, moduleId: str):
        checkCode = hashlib.sha256(specialCode + self.salt).hexdigest().encode()
        newSocket = socket.socket(account.socket.socket.family, account.socket.socket.type)
        newSocket.connect(self.messageTransfer.socket.getpeername())
        newSocket.send(checkCode)
        messageTransfer = MessageTransfer(self.messageTransfer.accountManager, newSocket, description=f'Module: {id_}')
        self.accountManager.getSelfAccount().addExtraConnection(id_, messageTransfer)
        account.addExtraConnection(id_, messageTransfer)
        self.accountManager.logs.sendLog(
            '[MCM Client] Accepted extra connection invite for module with id ' +
            f"{moduleId[:3]}...{moduleId[-3:]}.", -1
        )
        return messageTransfer
