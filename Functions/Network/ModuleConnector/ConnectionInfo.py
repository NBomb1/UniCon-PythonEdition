import socket


class ConnectionInfo:
    socketConnection: dict[int: socket.socket]
    transferConnection: dict[int: socket.socket]

    def __init__(self, s: socket.socket, port: int):
        self.s = s
        self.port = port
