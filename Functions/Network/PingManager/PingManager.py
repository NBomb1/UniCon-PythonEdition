from datetime import datetime
from os import urandom
from threading import Thread
from time import sleep

from Functions.ModuleHandler.moduleAPI import API
from Functions.Network.Accounts.AccountData import Account
from Functions.Network.Accounts.AccountDataManager import AccountManager
from Functions.Network.DataTransfer import MessageTransfer
from Functions.Network.ModuleConnector.Client.InviteConnectionInfo import InviteConnectionInfo
from Functions.Network.ModuleConnector.WaitingForConnectionInfo import WaitingForConnectionInfo


class Module:
    accountManager: AccountManager

    id_ = "sF6jA2wZ5tQ8xH3nM0iD7gK4pE9cV1oL2bN4vX7zY5rT1lQ3hU8yG9dS6fW2enw3"
    version = "0.0.1"
    name = "PingManager"
    author = "ArT"
    defaultNetworkAuth = True
    isOnlyUI = False

    def __init__(self, api: API):
        self.api = api
        self.logs = self.api.getLogs()
        self.logs.sendLog('[PingManager] Has been loaded!', -1)

    def getInfo(self, accountManager: AccountManager, isServer: bool):
        self.logs.sendLog(f'[PingManager] Getting info! isServer={isServer}', -1)
        self.accountManager = accountManager
        self.mcm = self.api.getConnectorManager()
        if isServer:
            self.api.getTriggerManager().accountAddedTrigger(self.startPing)
        # else:
        #     self.api.getTriggerManager().clientConnectedTrigger(self)

    def startPing(self, account: Account):
        self.logs.sendLog('[PingManager] Trying to establish to client.', -1)
        WaitingForConnectionInfo(
            self.id_,
            self.api.getConnectorManager().server.addConnectionWaiting,
            account,
            self.gotServerConnection
        )

    def mcm_inviteConnection(self, invite: InviteConnectionInfo):
        self.logs.sendLog('[PingManager] Accepting the invite...', -1)
        s: MessageTransfer = invite.accept()

        def echo():
            while True:
                self.logs.sendLog('[PingManager] Ping!', -1)
                s.socket.send(s.socket.recv(16))
                self.logs.sendLog('[PingManager] Pong!', -1)

        Thread(target=echo, daemon=True).start()

    def gotServerConnection(self, info: WaitingForConnectionInfo):
        socket = info.socket.socket

        def pingHandler():
            while True:
                self.logs.sendLog('[PingManager] Ping!', -1)
                code = urandom(16)
                start = datetime.now()
                socket.send(code)
                if socket.recv(16) == code:
                    res = int((datetime.now() - start).total_seconds() * 1000)
                    info.account.update_ping(res)
                    self.logs.sendLog(f'[PingManager] Pong {res}!', -1)
                else:
                    socket.close()
                    info.account.socket.socket.close()
                    return
                sleep(2)
        Thread(target=pingHandler, daemon=True).start()
