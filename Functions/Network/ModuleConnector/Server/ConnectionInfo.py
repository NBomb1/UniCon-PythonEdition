import hashlib
import socket
from os import urandom

from Functions.ModuleHandler.moduleAPI import API
from Functions.Network.Accounts.AccountData import Account
from Functions.Network.ModuleConnector.WaitingForConnectionInfo import WaitingForConnectionInfo


class ConnectionInfo:
    api: API
    socketConnection: dict[str: socket.socket] = {}  # id -> socket
    transferConnection: dict[str: socket.socket] = {}  # id -> transfer
    connections: dict[str: socket] = {}  # UserId -> socket

    def __init__(self, class_, maxListening: int):
        if len(class_.id_) != 128:
            raise ValueError("ID can't be unequal length of 128.")

        self.maxListening = maxListening
        self.moduleId = class_.id_
        self.api = class_.api

    def createConnection(self, account: Account, res: callable):
        specialCode = urandom(128)
        checkCode = hashlib.sha256(specialCode + account.salt).hexdigest().encode()
        account.socket.send_message(
            'ModuleConnector',
            id=self.moduleId,
            specialCode=specialCode
        )
        self.api.getConnectorManager().addConnectionWaiting(
            WaitingForConnectionInfo(
                checkCode,
                account,
                res
            )
        )
