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
from Functions.logManager.logManager import Logs


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
            message = s.recv(Info.preAuthMessageLength).decode()
            return message  # getting special message
        except socket.timeout:
            return None

    @staticmethod
    def authentication(account: PreAccount, password: str, s: socket.socket, logs: Logs, newAccount: callable) -> None:
        if (
                Authentication._1_PhaseRecognition(account.socket, logs) and  # Определение
                Authentication._2_PhaseBuiltInModuleCheck(account.socket, logs) and  # Проверка версий
                Authentication._3_PhasePasswordCheck(account.socket, password, logs) and  # Ввод пароля
                Authentication._4_PhaseAllModulesCheck(account.socket, logs) and  # Проверка аддонов
                Authentication._5_PhaseModuleConnection(account.socket, logs)  # Подключение аддонов
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

            newAccount(Account(
                socket=account.socket,
                ip=account.ip,
                port=account.port,
                nickname=nickname,
                pc_name=pc,
                id_=id_
            ))
            logs.sendLog("[MainChannel] Authentication went successfully", -1)

    @staticmethod
    def _1_PhaseRecognition(s: socket.socket, logs: Logs) -> bool:
        """Phase 1 - Recognition: We do not accept connections from others programs"""
        message = Authentication._getMessage(s)
        if message is None:
            s.close()
            return False
        message = message.replace(' ', '')  # formatting to built-in len default

        if message != Info.unique_message:  # checking if those aren't same
            s.send(Authentication._fillText("!!Connection restriction", Info.preAuthMessageLength).encode())
            s.close()
            logs.sendLog("[Authentication] Couldn't pass 1st authentication phase.", -1)
            return False

        logs.sendLog("[Authentication] First phase has been passed.", -1)
        return True

    @staticmethod
    def _2_PhaseBuiltInModuleCheck(s: socket.socket, logs: Logs) -> bool:
        """Phase 2 - BuiltIn module checking: We must have same versions"""
        message = Authentication._getMessage(s)
        if message is None:
            s.close()
            logs.sendLog("[Authentication] Couldn't pass 2nd authentication phase.", -1)
            return False
        try:
            message = literal_eval(message.replace(" ", ''))  # making it type of dict
        except ValueError:
            s.close()
            logs.sendLog("[Authentication] Couldn't pass 2nd authentication phase.", -1)
            return False

        modules = Info.getBuiltInModules()  # getting our module versions
        send = {}
        for i in modules:  # comparing versions from ours to client
            if modules[i] != message[i]:  # if version is not the same
                send[i] = modules[i]  # adding version message

        if send:  # checking if there are any issues with module versions
            s.send(send.__str__())  # sending our module versions
            s.close()  # and closing connection
            logs.sendLog("[Authentication] Couldn't pass 2nd authentication phase.", -1)
            return False

        logs.sendLog("[Authentication] Second phase has been passed.", -1)
        return True

    @staticmethod
    def _3_PhasePasswordCheck(s: socket.socket, password: str, logs: Logs) -> bool:
        """Phase 3 - Security check: Password check"""
        # Generating salt on the server
        client_salt = urandom(128)
        # Sending the salt to the client
        s.send(client_salt)
        hashed_password = hashlib.sha512(client_salt + password.encode()).hexdigest().encode()
        print(hashed_password)

        # Receiving the hashed password from the client
        for tries in range(3):
            received_hashed_password = s.recv(Info.preAuthMessageLength)  # Hashed password is 128 characters long
            if received_hashed_password is None:
                s.close()
                logs.sendLog(
                    f"[Authentication] Couldn't pass 3rd authentication phase. Connection has been closed.",
                    -1
                )
                return False

            if received_hashed_password == hashed_password:
                logs.sendLog("[Authentication] Third phase has been passed.", -1)
                s.send(Authentication._fillText("1", Info.preAuthMessageLength).encode())
                return True
            else:
                logs.sendLog(f"[Authentication] Couldn't pass 3rd authentication phase for {tries + 1} time.", -1)
                s.send(Authentication._fillText("", Info.preAuthMessageLength).encode())
        logs.sendLog(f"[Authentication] Client couldn't pass 3rd phase. Closing connection...", -1)
        s.close()
        return False

    @staticmethod
    def _4_PhaseAllModulesCheck(s: socket.socket, logs: Logs) -> bool:
        logs.sendLog("[Authentication] Fourth phase has been passed.", -1)
        return True

    @staticmethod
    def _5_PhaseModuleConnection(s: socket.socket, logs: Logs) -> bool:
        logs.sendLog("[Authentication] Fifth phase has been passed.", -1)
        return True
