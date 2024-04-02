from Functions.Exceptions.Account import Account
import socket as s


class SelfAccount:
    nickname: str
    pc_name: str
    id: str = None
    ping: int = None
    salt: bytes = None  # needs for modules and ect.

    def __init__(self, nickname: str, tags=None):
        self.nickname = nickname
        self.pc_name = s.gethostname()
        self.tags = tags if tags is not None else []

    def updateNickname(self, nickname: str):
        self.nickname = nickname

    def updatePing(self, ping: int):
        self.ping = ping

    def setId(self, id: str):
        if self.id is not None:
            raise Account.InfoUpdateException("Can't change id that was filled once.")
        self.id = id

    def setSalt(self, salt: bytes):
        if self.salt is not None:
            raise Account.InfoUpdateException("Can't change salt that was filled once.")
        self.salt = salt
