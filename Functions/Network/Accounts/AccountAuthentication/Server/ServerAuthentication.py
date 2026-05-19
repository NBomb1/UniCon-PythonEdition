import hashlib
from os import urandom
import socket

from typing import TYPE_CHECKING
from random import randint

# Importing authentication phases
from Functions.Network.Accounts.AccountAuthentication.Server.AuthenticationPhases._1_PhaseRecognition import \
    _1_PhaseRecognition
from Functions.Network.Accounts.AccountAuthentication.Server.AuthenticationPhases._2_PhaseBuiltInModuleCheck import \
    _2_PhaseBuiltInModuleCheck
from Functions.Network.Accounts.AccountAuthentication.Server.AuthenticationPhases._3_PhasePasswordCheck import \
    _3_PhasePasswordCheck
from Functions.Network.Accounts.AccountAuthentication.Server.AuthenticationPhases._4_PhaseDataShare import \
    _4_PhaseDataShare
from Functions.Network.Accounts.AccountAuthentication.Server.AuthenticationPhases._PhaseVerification import \
    _PhaseVerification

from Functions.Network.Accounts.AccountManager import AccountManager
from Functions.Network.DataTransfer import MessageTransfer
from Functions.Network.SecurityInfo import SecurityInfo
from Functions.Network.Accounts.AccountAuthentication.Server.PreAuthAccount import PreAccount
from Functions.Network.Accounts.AccountData import Account
from Functions.Network.ModuleConnector.ConnectorManager import ConnectorManager
from Functions.logManager import Logs

if TYPE_CHECKING:
    from Functions.Network.FileTransfer.FileTransfer import FileTransfer


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
                       accountManager: AccountManager, mcm: ConnectorManager, fileTransfer: 'FileTransfer') -> None:

        # Checking for special code
        if _1_PhaseRecognition(account, mcm, logs, Authentication, fileTransfer):  # Определение
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
                _2_PhaseBuiltInModuleCheck(account.socket, logs, Authentication) and  # Проверка версий
                Authentication._passInfo(s) and  # Успешное прохождение 2 фазы
                _3_PhasePasswordCheck(account.socket, password, logs, client_salt, Authentication)  # Ввод пароля
        ):

            # Обмен данных
            if (data := _4_PhaseDataShare(account.socket, logs, accountManager, Authentication)) is None:
                s.close()
                return
                # Authentication._5_PhaseAllModulesCheck(account.socket, logs) # Проверка аддонов
                # Authentication._6_PhaseModuleConnection(account.socket, logs)  # Подключение аддонов
            if not _PhaseVerification(logs, data, account, Authentication):  # checking data integrity
                return

            # Creating account
            account = Account(
                socket=MessageTransfer(
                    accountManager,
                    account.socket,
                    description='Client main channel (server side)'
                ),
                ip=account.ip,
                port=account.port,
                nickname=data['nickname'],
                pc_name=data['pc_name'],
                id_=data['id'],
                salt=client_salt
            )
            # registering types
            account.socket.registerType('account')
            account.socket.registerType('FileTransfer')
            account.socket.registerType('ModuleConnector')
            account.socket.registerType('close')

            # account.socket.registerFunction('FileTransfer', fileTransfer.mainChannelResponses)
            account.socket.registerFunction('close', accountManager._clientClosesConnectionWithReason)

            account.socket.senderHandler()
            account.socket.handleMessages()

            accountManager.add(account)
            logs.sendLog(f"[MainChannel] Authentication from "
                         f"{s.getpeername()[0]}:{s.getpeername()[1]} went successfully -> "
                         f"{account.nickname} | {account.id}", -1)

    @staticmethod
    def _passInfo(s: socket.socket) -> bool:
        s.send(Authentication._fillText('pass', SecurityInfo.preAuthMessageLength).encode())
        return True

    @staticmethod
    def createHashedPassword(salt: bytes, password: str) -> bytes:
        return hashlib.sha512(salt + password.encode()).hexdigest().encode()
