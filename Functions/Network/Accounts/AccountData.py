import socket as s


class Account:
    socket: s.socket
    ip: str
    port: int
    nickname: str
    pc_name: str
    id: str
    ping: int

    def __init__(
            self,
            socket: s.socket,
            ip: str,
            port: int,
            nickname: str,
            pc_name: str,
            id_: str,
            salt: bytes | None,
            tags: list = None
    ):
        self.socket = socket  # for server only
        self.ip = ip  # for server
        self.port = port  # for server
        self.nickname = nickname
        self.pc_name = pc_name
        self.id = id_
        self.salt = salt  # for server only
        self.ping = -1  # updates
        self.tags = tags if tags is not None else []  # can be used as special perms

    def update_ping(self, ping: int):
        self.ping = ping

    def updateNickname(self, nickname: str):
        self.nickname = nickname
