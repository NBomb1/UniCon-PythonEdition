import hashlib
from os import urandom

from Functions.Network.Accounts.AccountData import Account
from Functions.Network.DataTransfer import MessageTransfer


class WaitingForConnectionInfo:
    socket: MessageTransfer = None

    def __init__(self,
                 moduleId: str,
                 addConnection: callable,  # ModuleConnectorManager.addConnectionWaiting,
                 account: Account,
                 func: callable,
                 timeout=60
                 ):
        self.account = account
        self.func = func
        self.timeout = timeout
        self.moduleId = moduleId

        addConnection(self)
        specialCode = urandom(128)
        self.specialCode = hashlib.sha256(specialCode + account.salt).hexdigest().encode()
        account.socket.send_message(
            'ModuleConnector',
            id=self.moduleId,
            specialCode=specialCode
        )

    def setMessageTransfer(self, obj: MessageTransfer):
        if self.socket is None:
            self.socket = obj
