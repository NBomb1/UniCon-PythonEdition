import socket
import traceback

from Functions.Network.Accounts.AccountData import Account
from Functions.Network.Accounts.Client.AccountDataHandler import AccountDataHandler
from Functions.Network.Accounts.Server.AccountDataTransfer import AccountDataTransfer
from Functions.Network.Accounts.SelfAccount import SelfAccount
from Functions.Exceptions.Account import Account as AccountExc
from Functions.logManager import Logs


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

    def __init__(self, logs: Logs):
        self.logs = logs

    def startedAsServer(self):
        """Sets flag isServer to True"""
        self.owner = self.selfAccount

    def startedAsClient(self):
        """Sets flag isServer to False"""

    def closeConnection(self):
        """Sets isServer to None and clears manager."""
        self.logs.sendLog("[AccountManager] Closing connection...", -1)
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
        isServer = self.getIsServer()
        if isServer and len(self.participants) >= self.maxConnections:
            self.logs.sendLog(f"[AccountManager] Can't add more than allowed connections!", -1)
            account.socket.socket.close()
            return

        self.participants.append(account)
        if isServer:
            account.addUpdatedAccount(self._sendUpdatedInfo)
            self._sendAllInfo()
        for func in self.NewAccountTrigger:
            try:
                func(account)
            except TypeError:
                self.logs.sendLog(f"[AccountManager] Function has critical error! {traceback.format_exc()}", -1)

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

    def getOwner(self) -> Account:
        """Gets owner account."""
        return self.owner

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

    def selfAccountDisconnectedTriggerREMOVE(self, func: callable, ignoreException=False):
        """Removes function from trigger list."""
        if not ignoreException or func in self.SelfDisconnectTrigger:
            self.SelfDisconnectTrigger.remove(func)

    def _disconnectedFromServer(self, msg: dict[str, str]):
        """
        Calls all trigger functions if YOU disconnected from server.
        Do not use it.
        """
        for func in self.SelfDisconnectTrigger:
            func(msg)

    def getIsServer(self) -> bool | None:
        """Returns bool when AccountManager is active."""
        return (self.selfAccount is self.owner) if self.selfAccount is not None else None

    def clientStopped(self):
        for func in self.ClientStoppedTrigger:
            try:
                func()
            except Exception:
                traceback.print_exc()

    def serverStopped(self):
        for func in self.ServerStoppedTrigger:
            try:
                func()
            except Exception:
                traceback.print_exc()

    def serverStoppedTrigger(self, func: callable):
        self.ServerStoppedTrigger.append(func)

    def serverStoppedTriggerREMOVE(self, func: callable, ignoreException=False):
        if not ignoreException or func in self.ServerStoppedTrigger:
            self.ServerStoppedTrigger.remove(func)

    def clientStoppedTrigger(self, func: callable):
        self.ClientStoppedTrigger.append(func)

    def _clientClosesConnectionWithReason(self, msg: dict):
        """Do not use this function."""
        account: Account = msg['_account']
        try:
            reason = msg['reason']
            nickname = account.nickname
            id_ = account.id
            self.logs.sendLog(f'[AccountManager] Client {nickname}<{id_}> closed connection with reason: {reason}', -1)
        finally:
            self._disconnectAccount(account)
