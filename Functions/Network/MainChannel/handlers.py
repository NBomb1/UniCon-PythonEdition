import socket
import threading
from Functions.Server.PreAuthAccount import PreAccount
from Functions.Server.ServerAuthentication import Authentication


class Handlers:
    isWorking = False

    def __init__(self, s: socket.socket, password: str):
        self.socket = s
        self.password = password
        self._connectionFunctionTrigger = []

    def handleIncomingConnections(self):
        self.isWorking = True

        def thread():
            while self.isWorking:
                try:
                    account = PreAccount(self.socket.accept())  # Creating Pre Account for others modules
                    if not self.isWorking:  # checking if we still must accept connection
                        account.socket.close()  # closing connection if we shouldn't accept it
                        return  # stop working
                    for i in self._connectionFunctionTrigger:
                        i()  # getting all functions to call
                    Authentication.authentication(account, self.password)
                except socket.timeout:
                    pass

        threading.Thread(target=thread).start()

    def RegisterConnectionHandler(self, function: callable):
        self._connectionFunctionTrigger.append(function)
