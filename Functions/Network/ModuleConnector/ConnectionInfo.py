import socket


class ConnectionInfo:
    socketConnection: dict[int: socket.socket]
    transferConnection: dict[int: socket.socket]

    def __init__(self, s: socket.socket, ip: str, port: int, maxListening: int):
        self.s = s
        self.ip = ip
        self.port = port
        self.maxListening = maxListening
