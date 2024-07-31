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
from time import sleep

from Functions.Network.Accounts.AccountDataManager import AccountManager
from Functions.Network.DataTransfer import MessageTransfer
from Functions.Network.SecurityInfo import SecurityInfo
from Functions.Network.Accounts.AccountAuthentication.Server.PreAuthAccount import PreAccount
from Functions.Network.Accounts.AccountData import Account
from Functions.Network.ModuleConnector.ConnectorManager import ConnectorManager
from Functions.Tools.logManager import Logs


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
            message = s.recv(SecurityInfo.preAuthMessageLength).decode()
            return message  # getting special message
        except socket.timeout or ConnectionResetError or OSError:
            return None
        except ConnectionResetError:
            return None

    @staticmethod
    def authentication(account: PreAccount, password: str, s: socket.socket, logs: Logs,
                       accountManager: AccountManager, mcm: ConnectorManager) -> None:

        # Checking for special code
        if Authentication._1_PhaseRecognition(account, mcm, logs):  # Определение
            return

        #  checking if the server is full
        if len(accountManager.getParticipants()) >= accountManager.getMaxConnections():
            s.send(Authentication._fillText('The server is full.', SecurityInfo.preAuthMessageLength).encode())
            s.close()
            logs.sendLog('[Authentication] Restriction: The server is full.', -1)
            return

        client_salt = urandom(128)
        if (
                Authentication._passInfo(s) and  # Успешное прохождение 1 фазы
                Authentication._2_PhaseBuiltInModuleCheck(account.socket, logs) and  # Проверка версий
                Authentication._passInfo(s) and  # Успешное прохождение 2 фазы
                Authentication._3_PhasePasswordCheck(account.socket, password, logs, client_salt)  # Ввод пароля
        ):

            # Обмен данных
            if (data := Authentication._4_PhaseDataShare(account.socket, logs, accountManager)) is None:
                s.close()
                return
                # Authentication._5_PhaseAllModulesCheck(account.socket, logs) # Проверка аддонов
                # Authentication._6_PhaseModuleConnection(account.socket, logs)  # Подключение аддонов
            if not Authentication._PhaseVerification(logs, data, account):  # checking data integrity
                return

            # Creating account
            account = Account(
                socket=MessageTransfer(accountManager, account.socket),
                ip=account.ip,
                port=account.port,
                nickname=data['nickname'],
                pc_name=data['pc_name'],
                id_=data['id'],
                salt=client_salt
            )
            # registering types
            account.socket.registerType('account')
            account.socket.registerType('ModuleConnector')
            account.socket.registerType('close')

            account.socket.senderHandler()

            accountManager.add(account)
            logs.sendLog(f"[MainChannel] Authentication from "
                         f"{s.getpeername()[0]}:{s.getpeername()[1]} went successfully", -1)

    @staticmethod
    def _1_PhaseRecognition(account: PreAccount, mcm: ConnectorManager, logs: Logs) -> bool | None:
        """Phase 1 - Recognition: We do not accept connections from others programs."""
        message = Authentication._getMessage(account.socket)
        if message is None:
            account.socket.close()
            return True
        message = message.replace(' ', '')  # formatting to built-in len default
        if mcm.server.checkSpecialCode(message, account.socket):
            return True
        elif message != SecurityInfo.unique_message:  # checking if those aren't same
            account.socket.send(
                Authentication._fillText("!!Connection restriction", SecurityInfo.preAuthMessageLength).encode())
            logs.sendLog(f"[Authentication] Couldn't pass 1st authentication phase. "
                         f"{account.socket.getpeername()[0]}:{account.socket.getpeername()[1]}", -1)
            account.socket.close()
            return True

        logs.sendLog("[Authentication] First phase has been passed."
                     f"{account.socket.getpeername()[0]}:{account.socket.getpeername()[1]}", -1)
        return False

    @staticmethod
    def _2_PhaseBuiltInModuleCheck(s: socket.socket, logs: Logs) -> bool:
        """Phase 2 - BuiltIn module checking: We must have same versions"""
        message = Authentication._getMessage(s)
        if message is None:
            s.close()
            logs.sendLog("[Authentication] Couldn't pass 2nd authentication phase."
                         f"{s.getpeername()[0]}:{s.getpeername()[1]}", -1)
            return False
        try:
            message = literal_eval(message.replace(" ", ''))  # making it type of dict
        except ValueError:
            s.close()
            logs.sendLog("[Authentication] Couldn't pass 2nd authentication phase."
                         f"{s.getpeername()[0]}:{s.getpeername()[1]}", -1)
            return False

        modules = SecurityInfo.getBuiltInModules()  # getting our module versions
        send = {}
        for i in modules:  # comparing versions from ours to client
            if modules[i] != message[i]:  # if version is not the same
                send[i] = modules[i]  # adding version message

        if send:  # checking if there are any issues with module versions
            s.send(send.__str__())  # sending our module versions
            s.close()  # and closing connection
            logs.sendLog("[Authentication] Couldn't pass 2nd authentication phase."
                         f"{s.getpeername()[0]}:{s.getpeername()[1]}", -1)
            return False

        logs.sendLog("[Authentication] Second phase has been passed."
                     f"{s.getpeername()[0]}:{s.getpeername()[1]}", -1)
        return True

    @staticmethod
    def _3_PhasePasswordCheck(s: socket.socket, password: str, logs: Logs, client_salt: bytes) -> bool:
        """Phase 3 - Security check: Password check"""
        # Sending the salt to the client
        s.send(client_salt)

        # creating password hash
        hashed_password = hashlib.sha512(client_salt + password.encode()).hexdigest().encode()

        # Receiving the hashed password from the client
        allowed_tries = 3
        current_tries = 0
        defaultPasswordChecked = False
        while current_tries < allowed_tries:
            current_tries += 1
            # Getting password hash from client
            try:
                # Hashed password is 128 characters long
                received_hashed_password = s.recv(SecurityInfo.preAuthMessageLength)
            except ConnectionAbortedError:  # Client can disconnect from server before logging in
                received_hashed_password = None
            except ConnectionResetError:  # Client can disconnect from server before logging in
                received_hashed_password = None

            # Checking is password is not given
            if received_hashed_password is None:
                s.close()
                logs.sendLog(
                    f"[Authentication] Couldn't pass 3rd authentication phase. Client disconnected."
                    f"{s.getpeername()[0]}:{s.getpeername()[1]}", -1)
                return False

            # If given password hash is the same as our password hash
            if received_hashed_password == hashed_password:
                logs.sendLog("[Authentication] Third phase has been passed."
                             f"{s.getpeername()[0]}:{s.getpeername()[1]}", -1)
                s.send(Authentication._fillText("1", SecurityInfo.preAuthMessageLength).encode())
                return True
            else:
                if current_tries < allowed_tries:
                    s.send(Authentication._fillText("", SecurityInfo.preAuthMessageLength).encode())
                if (
                        received_hashed_password.decode()
                        ==
                        Authentication.createHashedPassword(client_salt, SecurityInfo.defaultPassword).decode()
                        and not defaultPasswordChecked
                ):
                    defaultPasswordChecked = True
                    current_tries -= 1
                    continue
                defaultPasswordChecked = True
                logs.sendLog(f"[Authentication] Couldn't pass 3rd authentication phase for {current_tries} time."
                             f"{s.getpeername()[0]}:{s.getpeername()[1]}", -1)

        logs.sendLog(f"[Authentication] Client couldn't pass 3rd phase. Closing connection..."
                     f"{s.getpeername()[0]}:{s.getpeername()[1]}", -1)
        s.send(Authentication._fillText("Too many attempts", SecurityInfo.preAuthMessageLength).encode())
        sleep(10)
        s.close()
        return False

    @staticmethod
    def _4_PhaseDataShare(s: socket.socket, logs: Logs, accountManager: AccountManager) -> dict | None:
        # 1. Getting pc_name and nickname
        # 2. Sending id
        # 3. Sending AllAccounts info

        # Getting nickname
        nickname = Authentication._getMessage(s).rstrip(' ')
        pc_name = Authentication._getMessage(s).rstrip(' ')
        if nickname is None or pc_name is None:
            s.close()
            return None
        id_ = Authentication.generate_random_id(8)

        # Sending its id to client
        s.send(Authentication._fillText(id_, SecurityInfo.preAuthMessageLength).encode())

        # Sending all accounts info
        accountInfo = accountManager.getAllInfoAccount([]).__str__()
        s.send(Authentication._fillText(accountInfo, SecurityInfo.preAuthGetAccountInfo).encode())

        logs.sendLog("[Authentication] Forth phase has been passed."
                     f"{s.getpeername()[0]}:{s.getpeername()[1]}", -1)
        return {
            'id': id_,
            'nickname': nickname,
            'pc_name': pc_name
        }

    @staticmethod
    def _5_PhaseAllModulesCheck(s: socket.socket, logs: Logs) -> bool:
        logs.sendLog("[Authentication] Fifth phase has been passed."
                     f"{s.getpeername()[0]}:{s.getpeername()[1]}", -1)
        return True

    @staticmethod
    def _PhaseVerification(logs: Logs, data: dict, account: PreAccount) -> bool:
        if len(data['nickname']) > 30 or len(data['nickname']) < 3:
            account.socket.send(Authentication._fillText("Nickname must be between 3 and 30 symbols.",
                                                         SecurityInfo.preAuthMessageLength).encode())
            logs.sendLog(f"[Authentication] Couldn't pass authentication verification phase. "
                         f"{account.socket.getpeername()[0]}:{account.socket.getpeername()[1]}", -1)
            account.socket.close()
            return False
        if len(data['pc_name']) > 50 or len(data['pc_name']) < 2:
            account.socket.send(Authentication._fillText("PC name must be between 2 and 50 symbols.",
                                                         SecurityInfo.preAuthMessageLength).encode())
            logs.sendLog(f"[Authentication] Couldn't pass authentication verification phase. "
                         f"{account.socket.getpeername()[0]}:{account.socket.getpeername()[1]}", -1)
            account.socket.close()
            return False
        return True

    @staticmethod
    def _6_PhaseModuleConnection(s: socket.socket, logs: Logs) -> bool:
        logs.sendLog("[Authentication] Sixth phase has been passed."
                     f"{s.getpeername()[0]}:{s.getpeername()[1]}", -1)
        return True

    @staticmethod
    def _passInfo(s: socket.socket) -> bool:
        s.send(Authentication._fillText('pass', SecurityInfo.preAuthMessageLength).encode())
        return True

    @staticmethod
    def createHashedPassword(salt: bytes, password: str) -> bytes:
        return hashlib.sha512(salt + password.encode()).hexdigest().encode()
