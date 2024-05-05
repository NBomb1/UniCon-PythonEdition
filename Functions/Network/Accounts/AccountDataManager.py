import socket

from Functions.Network.Accounts.AccountData import Account
from Functions.Network.Accounts.AccountDataTransfer import AccountDataTransfer
from Functions.Network.Accounts.SelfAccount import SelfAccount


class AccountManager(AccountDataTransfer):
    _NewAccountTrigger = []
    _DisconnectAccountTrigger = []
    _selfDisconnectTrigger = []
    participants: list[Account] = []
    selfAccount: SelfAccount
    maxConnections: int

    def add(self, account: Account):
        """Adds new account. Calls trigger functions."""
        if len(self.participants) >= self.maxConnections:
            account.socket.socket.close()
            return

        self.participants.append(account)
        for func in self._NewAccountTrigger:
            func(account)

    def findID(self, id_: str) -> Account | None:
        """Tries to find account. If not found returns None."""
        for i in self.participants:
            if i.id == id_:
                return i
        return None

    def getSelfAccount(self):
        """Gets Self Account. Info of your account."""
        return self.selfAccount

    def addNewAccountFunction(self, func: callable):
        """Adds function to trigger list."""
        self._NewAccountTrigger.append(func)

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
        assert account in self.participants
        for func in self._DisconnectAccountTrigger:
            func(account)

        for i in account.extraConnections.values():
            for conn in i:
                conn.socket.close()

        account.socket.socket.close()
        self.participants.remove(account)

    def kickAccount(self, actionMaker: Account, account: Account, reason='No reason was given.'):
        """Kicks an account. Works only for server.(now)"""
        account.socket.send_message(
            type_='close',
            thread=False,
            disconnectType='kick',
            id=actionMaker.id,
            nickname=actionMaker.nickname,
            reason=reason
        )
        self._disconnectAccount(account)

    def accountDisconnectedTrigger(self, func: callable):
        """
        Adds function to trigger list.
        Calls when SOMEONE disconnected from server.
        """
        self._DisconnectAccountTrigger.append(func)

    def selfAccountDisconnectedTrigger(self, func: callable):
        """
        Adds function to trigger list.
        Calls when YOU disconnected from server.
        """
        self._selfDisconnectTrigger.append(func)

    def _disconnectedFromServer(self, msg: dict[str, str]):
    # def disconnectedFromServer(self, *args, **kwargs):
        """
        Calls all trigger functions if YOU disconnected from server.
        """
        print(msg)
        for func in self._selfDisconnectTrigger:
            func(msg)
