import socket


class MessageTransfer:
    types = []

    def __init__(self, s: socket.socket):
        self.socket = s

    def registerType(self, type_: str):
        self.types.append(type_)

    def send_message(self, **kwargs):
        for i in kwargs:
            if i not in self.types:
                raise Exception('Type "' + i + '" is not in the types list.')

        message = len(kwargs).__str__() + kwargs.__str__()

        self.socket.send(message.encode())
