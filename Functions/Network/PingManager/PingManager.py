import random
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
        self.api.getAccountManager().serverStoppedTrigger(self.closedConnection)
        # self.logs.sendLog('[PingManager] Has been loaded!', -1)

    def getInfo(self, accountManager: AccountManager, isServer: bool):
        self.logs.sendLog(f'[PingManager] Getting info! isServer={isServer}', -1)
        self.accountManager = accountManager
        self.mcm = self.api.getConnectorManager()
        if isServer:
            self.api.getTriggerManager().accountAddedTrigger(self.startPing)
        # else:
        #     self.api.getTriggerManager().clientConnectedTrigger(self)

    def startPing(self, account: Account):
        """Server function"""
        self.logs.sendLog('[PingManager] Trying to establish to client.', -1)
        print('1salt:', account.salt)
        WaitingForConnectionInfo(
            self.id_,
            self.api.getConnectorManager().server.addConnectionWaiting,
            account,
            self.gotServerConnection
        )

    def mcm_inviteConnection(self, invite: InviteConnectionInfo):
        """Server Function - sends unique code to client and waits for response."""
        self.logs.sendLog('[PingManager] Accepting the invite...', -1)
        s: MessageTransfer = invite.accept()

        def echo():
            try:
                while True:
                    msg = s.socket.recv(16)
                    sleep(random.randint(1, 500) / 1000)  # creating random fake latency for tests
                    # s.socket.send(msg.upper() if random.randint(0, 5) == 1 else msg)
                    s.socket.send(msg)
                    # s.socket.send(s.socket.recv(16))
            except (ConnectionAbortedError, OSError):
                self.api.getTriggerManager().accountManager.closeConnection()

        Thread(target=echo, daemon=True).start()

    def gotServerConnection(self, info: WaitingForConnectionInfo):
        """Client Function - waits for server special code and sends it back."""
        socket = info.socket.socket

        def pingHandler():
            try:
                while True:
                    code = urandom(16)
                    start = datetime.now()
                    socket.send(code)
                    if (recv := socket.recv(16)) == code:
                        res = int((datetime.now() - start).total_seconds() * 1000)
                        info.account.update_ping(res)
                    else:
                        # print('closing connection!!!!', recv)
                        self.accountManager.kickAccount(
                            self.accountManager.getSelfAccount(),
                            info.account,
                            'PingManager got wrong info',
                            True
                        )
                        return
                    sleep(2)
            except (ConnectionResetError, OSError):
                # print('kicking an account')
                self.accountManager.kickAccount(
                    self.accountManager.getSelfAccount(),
                    info.account,
                    'Client disconnected from ping channel',
                    True
                )

        Thread(target=pingHandler, daemon=True).start()

    def closedConnection(self):
        """must be done correctly"""
        print('Function closedConnection in PingManager was ran!')
        if self.startPing in self.api.getAccountManager().NewAccountTrigger:
            self.api.getAccountManager().NewAccountTrigger.remove(self.startPing)
