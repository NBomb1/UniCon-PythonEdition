import socket as s


class Account:
    socket: s.socket
    ip: str
    port: int
    nickname: str
    pc_name: str
    id: str
    ping: int

    def __init__(self, socket: s.socket, ip: str, port: int, nickname: str, pc_name: str, id_: str, salt: bytes | None):
        self.socket = socket
        self.ip = ip
        self.port = port
        self.nickname = nickname
        self.pc_name = pc_name
        self.id = id_
        self.salt = salt  # for server only

    def update_ping(self, ping: int):
        self.ping = ping

    def updateNickname(self, nickname: str):
        self.nickname = nickname
