import socket as s


class Account:
    def __init__(self, socket: s.socket, ip: str, port: int, nickname: str, pc_name: str, id_: str):
        self.socket = socket
        self.ip = ip
        self.port = port
        self.nickname = nickname
        self.pc_name = pc_name
        self.id = id_
