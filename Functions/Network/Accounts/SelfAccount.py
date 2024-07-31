from threading import Thread

from Functions.Exceptions.Account import Account
import socket as s

from Functions.Network.DataTransfer import MessageTransfer


class SelfAccount:
    # all possible given arguments by default
    what_pc_name = 'pc_name'
    what_id = 'id'
    what_ip = 'ip'
    what_port = 'port'

    what_nickname = 'nickname'
    what_ping = 'ping'
    what_tag = 'tags'
    what_conn = 'extraConnections'

    nickname: str
    pc_name: str
    id: str = None
    ping: int = None
    salt: bytes = None  # needs for modules and ect.
    accountUpdatedTrigger: list[callable] = []
    extraConnections: dict[str, list[MessageTransfer]] = {}
    socket: MessageTransfer = None

    def __init__(self, nickname: str, tags=None):
        self.nickname = nickname
        self.pc_name = s.gethostname()
        self.tags = tags if tags is not None else []

    def __str__(self) -> str:
        return f"Nickname: {self.nickname}, ID: {self.id}"

    def setId(self, id: str):
        if self.id is not None:
            raise Account.InfoUpdateException("Can't change id that was filled once.")
        self.id = id

    def setSalt(self, salt: bytes):
        if self.salt is not None:
            raise Account.InfoUpdateException("Can't change salt that was filled once.")
        self.salt = salt

    def update_ping(self, ping: int):
        if self.ping == ping:
            return
        self.ping = ping
        self.accountHasBeenUpdated('ping')

    def addTag(self, tag: str):
        if not tag:
            raise ValueError(f"tag can't be empty!")
        if tag in self.tags:
            raise ValueError(f"tag {tag} is already in list!\nlist: {self.tags}\ntag: '{tag}'")
        if tag[0] == '_':
            raise ValueError(f"tag {tag} can't start with '_'!")

        self.tags.append(tag)
        self.accountHasBeenUpdated(self.what_tag)

    def removeTag(self, tag: str):
        if tag not in self.tags:
            raise ValueError(f"tag {tag} is not in list!\nlist: {self.tags}\ntag: '{tag}'")
        self.tags.remove(tag)
        self.accountHasBeenUpdated(self.what_tag)

    def updateTags(self, tags: list):
        self.tags.clear()
        for tag in tags:
            self.addTag(tag)

    def updateNickname(self, nickname: str):
        if nickname == self.nickname:
            return
        self.nickname = nickname
        self.accountHasBeenUpdated(self.what_nickname)

    def updatePcName(self, pc_name: str):
        if pc_name == self.pc_name:
            return
        self.pc_name = pc_name
        self.accountHasBeenUpdated(self.what_pc_name)

    def addExtraConnection(self, moduleId: str, s: MessageTransfer):
        self.extraConnections.setdefault(moduleId, []).append(s)
        self.accountHasBeenUpdated(self.what_conn)

    def removeExtraConnectionExact(self, moduleId: str, s: MessageTransfer):
        self.extraConnections.get(moduleId).remove(s)
        try:
            s.socket.close()
        except OSError:
            pass
        self.accountHasBeenUpdated(self.what_conn)

    def removeExtraConnection(self, s: MessageTransfer):
        copyKeys = self.extraConnections.copy().keys()
        for key in copyKeys:
            for conn in self.extraConnections[key]:
                if s == conn:
                    try:
                        conn.socket.close()
                    except OSError:
                        pass
                    self.extraConnections.get(key).remove(conn)
        self.accountHasBeenUpdated(self.what_conn)

    def addUpdatedAccount(self, func: callable):
        self.accountUpdatedTrigger.append(func)

    def removeUpdatedAccount(self, func: callable):
        self.accountUpdatedTrigger.remove(func)

    def accountHasBeenUpdated(self, what: str):
        if what == self.what_conn:
            copyKeys = self.extraConnections.copy().keys()
            for i in copyKeys:
                if not self.extraConnections.get(i):
                    self.extraConnections.pop(i)

        for func in self.accountUpdatedTrigger:
            Thread(target=func, args=(self, what), daemon=True).start()

    def setSocket(self, socket: MessageTransfer):
        self.socket = socket
