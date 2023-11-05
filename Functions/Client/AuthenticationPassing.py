import hashlib
import socket as s

from Functions.Network.MainChannel.Info import Info
from Functions.logManager.logManager import Logs


class Authentication:
    def __init__(self, socket: s.socket, logs: Logs, password: str, askPassword: callable):
        self.socket = socket
        self.logs = logs
        self.password = password
        self.askPassword = askPassword

    def start(self):
        self.logs.sendLog("[MainChannel Client] Trying to pass 1st phase.", -1)
        self.sendMessage(Info.unique_message, Info.preAuthMessageLength)

        self.logs.sendLog("[MainChannel Client] Trying to pass 2nd phase.", -1)
        self.sendMessage(Info.getBuiltInModules().__str__(), Info.preAuthMessageLength)

        self.logs.sendLog("[MainChannel Client] Trying to pass 3rd phase.", -1)
        salt = self.socket.recv(Info.preAuthMessageLength)  # receiving salt

        hashed_password = hashlib.sha512(salt + self.password.encode()).hexdigest()
        self.socket.send(hashed_password.encode())

        while not bool(self._getMessage().replace(' ', '')):
            try:
                self.socket.send(hashlib.sha512(salt + (self.askPassword()).encode()).hexdigest().encode())
            except TypeError:
                self.socket.close()
                self.logs.sendLog("[MainChannel Client] Connection closed.", -1)

    def sendMessage(self, message: str, count: int) -> int:
        return self.socket.send((message + (" " * (count - len(message)))).encode())

    def _getMessage(self) -> str | None:
        try:
            message = self.socket.recv(Info.preAuthMessageLength)
            print(message)
            return message.decode()  # getting special message
        except s.timeout:
            return None
