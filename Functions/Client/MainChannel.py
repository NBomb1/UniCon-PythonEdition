from Functions.Client.AuthenticationPassing import Authentication
from Functions.Network.MainChannel.Info import Info
from Functions.logManager.logManager import Logs
import socket as s


class ClientMainChannel:
    socket: s = None

    def __init__(self, logs: Logs, ip: str, port: int, askPassword: callable, password: str | None):
        self.logs = logs
        self.askPassword = askPassword
        logs.sendLog(f"Connecting to server {ip}:{port}", -1)

        if password is None:
            password = Info.defaultPassword
            self.logs.sendLog("[MainChannel Client] Using default password.", -1)
        else:
            self.logs.sendLog("[MainChannel Client] Using custom password.", -1)

        self.logs.sendLog("[MainChannel Client] Creating socket...", -1)
        self.socket = s.socket()
        self.logs.sendLog("[MainChannel Client] Connecting to the server...", -1)
        self.socket.connect((ip, port))
        Authentication(self.socket, self.logs, password, self.askPassword).start()
