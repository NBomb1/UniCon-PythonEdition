import socket
from typing import TYPE_CHECKING

from Functions.Network.Accounts.AccountDataManager import AccountManager
from Functions.Network.SecurityInfo import SecurityInfo
from Functions.logManager import Logs

if TYPE_CHECKING:
    from Functions.Network.Accounts.AccountAuthentication.Server.ServerAuthentication import Authentication as Auth


def _4_PhaseDataShare(s: socket.socket, logs: Logs, accountManager: AccountManager, Authentication: 'Auth') -> dict | None:
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
