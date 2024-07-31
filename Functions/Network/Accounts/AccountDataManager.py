import socket

from Functions.Network.Accounts.AccountData import Account
from Functions.Network.Accounts.Client.AccountDataHandler import AccountDataHandler
from Functions.Network.Accounts.Server.AccountDataTransfer import AccountDataTransfer
from Functions.Network.Accounts.SelfAccount import SelfAccount
from Functions.Exceptions.Account import Account as AccountExc


class AccountManager(AccountDataTransfer, AccountDataHandler):
    NewAccountTrigger = []
    DisconnectAccountTrigger = []
    SelfDisconnectTrigger = []
    ServerStoppedTrigger = []
    ClientStoppedTrigger = []

    participants: list[Account] = []
    selfAccount: SelfAccount | None = None
    maxConnections: int
    owner: Account | SelfAccount | None = None

    def __init__(self, logs):
        self.logs = logs

    def startedAsServer(self):
        """Sets flag isServer to True"""
        self.owner = self.selfAccount

    def startedAsClient(self):
        """Sets flag isServer to False"""

    def closeConnection(self):
        """Sets isServer to None and clears manager."""
        if self.getIsServer() is None:
            return

        if self.getIsServer():
            self.serverStopped()
            for i in self.participants:
                self.kickAccount(self.getSelfAccount(), i, 'Server closed', True)
            self._disconnectSelfAccount()
        elif not self.getIsServer():
            self.clientStopped()
            for i in self.participants:
                self._disconnectAccount(i)
            self._disconnectSelfAccount()

        self.logs.sendLog("[AccountManager] Connection successfully closed.", -1)

        self.owner = None

    def add(self, account: Account):
        """Adds new account. Calls trigger functions."""
        if self.getIsServer() and len(self.participants) >= self.maxConnections:
            account.socket.socket.close()
            return

        self.participants.append(account)
        if self.getIsServer():
            account.addUpdatedAccount(self._sendUpdatedInfo)
        for func in self.NewAccountTrigger:
            func(account)

    def findByID(self, id_: str) -> Account | SelfAccount | None:
        """Tries to find account. If not found returns None."""
        if self.selfAccount.id == id_:
            return self.selfAccount
        for i in self.participants:
            if i.id == id_:
                return i
        return None

    def getSelfAccount(self):
        """Gets Self Account. Info of your account."""
        return self.selfAccount

    def addNewAccountFunction(self, func: callable):
        """Adds function to trigger list."""
        self.NewAccountTrigger.append(func)

    def setSelfAccount(self, selfAccount: SelfAccount):
        """Sets Self Account. Info of your account."""
        self.selfAccount = selfAccount

    def setMaxConnections(self, maxConnections: int):
        """Sets max connections"""
        self.maxConnections = maxConnections

    def getMaxConnections(self) -> int:
        """Returns max count of connections"""
        return self.maxConnections

    def getParticipants(self) -> list[Account]:
        """Gets list of participants"""
        return self.participants

    def findBySocket(self, s: socket.socket) -> Account:
        """Works only for server side."""
        for i in self.participants:
            if i.socket.socket == s:
                return i
            for socketList in i.extraConnections.values():
                for socket_ in socketList:
                    if socket_ == s:
                        return i

    def _disconnectAccount(self, account: Account):
        """
        1. Removes all connections.
        2. Calls trigger functions.
        Works only for server side.
        """
        try:
            self.participants.remove(account)
        except ValueError:
            return

        # assert account in self.participants
        for func in self.DisconnectAccountTrigger:
            func(account)
        self.logs.sendLog(f'[AccountManager] Kicking from the server {account.id}', 0)
        account.removeAllConnections(self.getSelfAccount())
        if self.getIsServer():
            self.logs.sendLog('[AccountManager] Kicking from the server', 0)

            account.socket.socket.close()
        if self.selfAccount is not None:
            self.selfAccount.accountHasBeenUpdated(self.selfAccount.what_conn)

    def _disconnectSelfAccount(self):
        if self.selfAccount is None:
            return
        temp = self.selfAccount
        self.selfAccount = None

        for i in temp.extraConnections.values():
            for _ in i:
                _.socket.close()
        temp.extraConnections.clear()
        try:
            temp.socket.socket.close()
        except AttributeError:
            pass
        for func in self.DisconnectAccountTrigger:
            func(temp)

    def kickAccount(self, actionMaker: Account | SelfAccount, kickingAccount: Account, reason='No reason given.',
                    ignoreException=False):
        """Kicks an account. Works only for server.(now)"""
        if actionMaker == kickingAccount:
            raise AccountExc.KickingException("You cant kick yourself!")

        if kickingAccount not in self.participants:
            if not ignoreException:
                raise AccountExc.KickingException("Account is already disconnected.")
            return
        if self.getIsServer() is None:
            if not ignoreException:
                raise AccountExc.AccountManagerError('AccountManager is not active.')
            return

        kickingAccount.socket.send_message(
            type_='close',
            thread=False,
            disconnectType='kick',
            id=actionMaker.id,
            nickname=actionMaker.nickname,
            reason=reason
        )
        self._disconnectAccount(kickingAccount)

    def accountDisconnectedTrigger(self, func: callable):
        """
        Adds function to trigger list.
        Calls when SOMEONE disconnected from server.
        """
        self.DisconnectAccountTrigger.append(func)

    def selfAccountDisconnectedTrigger(self, func: callable):
        """
        Adds function to trigger list.
        Calls when YOU disconnected from server.
        """
        self.SelfDisconnectTrigger.append(func)

    def _disconnectedFromServer(self, msg: dict[str, str]):
        # def disconnectedFromServer(self, *args, **kwargs):
        """
        Calls all trigger functions if YOU disconnected from server.
        Do not use it.
        """
        for func in self.SelfDisconnectTrigger:
            func(msg)

    def getIsServer(self) -> bool | None:
        """Returns bool is AccountManager is active."""
        return (self.selfAccount == self.owner) if self.selfAccount is not None else None

    def clientStopped(self):
        for func in self.ClientStoppedTrigger:
            func()

    def serverStopped(self):
        for func in self.ServerStoppedTrigger:
            func()

    def serverStoppedTrigger(self, func: callable):
        self.ServerStoppedTrigger.append(func)

    def clientStoppedTrigger(self, func: callable):
        self.ClientStoppedTrigger.append(func)
