"""
- Authentication module.
- Has 5 phases of authentication.
- Failing one of them cause kicking from server.
"""
import hashlib
from os import urandom
import socket

from ast import literal_eval
from random import randint

from Functions.Network.MainChannel.Info import Info
from Functions.Server.PreAuthAccount import PreAccount
from Functions.Server.Account import Account
from Functions.Server.ServerPrefences import ServerInformation


class Authentication:
    @staticmethod
    def generate_random_id(length):
        random_id = ''.join([str(randint(0, 9)) for _ in range(length)])
        return random_id

    @staticmethod
    def _fillText(text: str, count: int):
        return text + (" " * (count - len(text)))

    @staticmethod
    def _getMessage(s: socket.socket) -> str | None:
        try:
            return s.recv(Info.preAuthMessageLength).decode()  # getting special message
        except socket.timeout:
            return None

    @staticmethod
    def authentication(account: PreAccount, server: ServerInformation, s: socket.socket) -> None:
        if (
                Authentication._1_PhaseRecognition(account.socket) and  # Определение
                Authentication._2_PhaseBuiltInModuleCheck(account.socket) and  # Проверка версий
                Authentication._3_PhasePasswordCheck(account.socket, server.password) and  # Ввод пароля
                Authentication._4_PhaseAllModulesCheck(account.socket) and  # Проверка аддонов
                Authentication._5_PhaseModuleConnection(account.socket)  # Подключение аддонов
        ):
            nickname = Authentication._getMessage(s)
            if nickname is None:
                account.socket.close()
                return
            pc = Authentication._getMessage(s)
            if pc is None:
                account.socket.close()
                return
            id_ = Authentication.generate_random_id(8)

            account.socket.send(Authentication._fillText(id_, Info.preAuthMessageLength))

            server.handler.newAccount(Account(
                socket=account.socket,
                ip=account.ip,
                port=account.port,
                nickname=nickname,
                pc_name=pc,
                id_=id_
            ))

    @staticmethod
    def _1_PhaseRecognition(s: socket.socket) -> bool:
        """Phase 1 - Recognition: We do not accept connections from others programs"""
        message = Authentication._getMessage(s)
        if message is None:
            s.close()
            return False
        message = message.replace(' ', '')  # formatting to built-in len default

        if message != Info.unique_message:  # checking if those aren't same
            s.send(Authentication._fillText("!!Connection restriction", Info.preAuthMessageLength).encode())
            s.close()
            return False

        return True

    @staticmethod
    def _2_PhaseBuiltInModuleCheck(s: socket.socket) -> bool:
        """Phase 2 - BuiltIn module checking: We must have same versions"""
        message = Authentication._getMessage(s)
        if message is None:
            s.close()
            return False

        message = literal_eval(message.replace(" ", ''))  # making it type of dict
        modules = Info.getBuiltInModules()  # getting our module versions
        send = {}
        for i in modules:  # comparing versions from ours to client
            if modules[i] != message[i]:  # if version is not the same
                send[i] = modules[i]  # adding version message

        if send:  # checking if there are any issues with module versions
            s.send(send.__str__())  # sending our module versions
            s.close()  # and closing connection
            return False
        return True

    @staticmethod
    def _3_PhasePasswordCheck(s: socket.socket, password: str) -> bool:
        """Phase 3 - Security check: Password check"""
        # Generating salt on the server
        client_salt = urandom(16)
        s.send(client_salt)  # Sending the salt to the client

        # Receiving the hashed password from the client
        received_hashed_password = Authentication._getMessage(s)  # Assuming the hashed password is 128 characters long
        if received_hashed_password is None:
            s.close()
            return False

        hashed_password = hashlib.sha512(client_salt + password.encode('utf-8')).digest()

        if received_hashed_password == hashed_password:
            return True
        else:
            s.close()
            return False

    @staticmethod
    def _4_PhaseAllModulesCheck(s: socket.socket) -> bool:
        return True

    @staticmethod
    def _5_PhaseModuleConnection(s: socket.socket) -> bool:
        return True
