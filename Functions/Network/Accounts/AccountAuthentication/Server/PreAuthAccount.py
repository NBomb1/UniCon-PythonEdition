import socket


class PreAccount:
    def __init__(self, info: tuple):
        self.socket: socket.socket = info[0]
        self.ip: str = info[1][0]
        self.port: int = info[1][1]
