from Functions.Exceptions.Account import Account
import socket as s

from Functions.Network.DataTransfer import MessageTransfer


class SelfAccount:
    nickname: str
    pc_name: str
    id: str = None
    ping: int = None
    salt: bytes = None  # needs for modules and ect.
    accountUpdated: list[callable] = []
    extraConnections: dict[str, list[MessageTransfer]] = {}

    def __init__(self, nickname: str, tags=None):
        self.nickname = nickname
        self.pc_name = s.gethostname()
        self.tags = tags if tags is not None else []

    def updateNickname(self, nickname: str):
        self.nickname = nickname
        self.accountHasBeenUpdated()

    def update_ping(self, ping: int):
        if self.ping != ping:
            self.ping = ping
            self.accountHasBeenUpdated()

    def setId(self, id: str):
        if self.id is not None:
            raise Account.InfoUpdateException("Can't change id that was filled once.")
        self.id = id

    def setSalt(self, salt: bytes):
        if self.salt is not None:
            raise Account.InfoUpdateException("Can't change salt that was filled once.")
        self.salt = salt

    def addUpdatedAccount(self, func: callable):
        self.accountUpdated.append(func)

    def removeUpdatedAccount(self, func: callable):
        self.accountUpdated.append(func)

    def accountHasBeenUpdated(self):
        for func in self.accountUpdated:
            func(self)

    def addExtraConnection(self, moduleId: str, s: MessageTransfer):
        self.extraConnections.setdefault(moduleId, [s])
        self.accountHasBeenUpdated()

    def removeExtraConnection(self, moduleId: str, s: MessageTransfer):
        self.extraConnections.setdefault(moduleId, [s])
        self.accountHasBeenUpdated()
