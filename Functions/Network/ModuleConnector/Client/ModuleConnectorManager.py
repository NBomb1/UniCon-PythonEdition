import hashlib
import socket
from functools import partial

from Functions.ModuleHandler.moduleHandler import ModuleHandler
from Functions.Network.DataTransfer import MessageTransfer
from Functions.Network.ModuleConnector.Client.InviteConnectionInfo import InviteConnectionInfo


class ClientModuleConnectorManager:
    def __init__(self, s: MessageTransfer, moduleHandler: ModuleHandler):
        self.moduleHandler = moduleHandler
        self.messageTransfer = s
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
                    partial(self.__accept, message['specialCode'])
                ))

    def __accept(self, specialCode: bytes):
        checkCode = hashlib.sha256(specialCode + self.salt).hexdigest().encode()
        newSocket = socket.socket()
        newSocket.connect(self.messageTransfer.socket.getpeername())
        newSocket.send(checkCode)
        return MessageTransfer(self.messageTransfer.accountManager, newSocket)
