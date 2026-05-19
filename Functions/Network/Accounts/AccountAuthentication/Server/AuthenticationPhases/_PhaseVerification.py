from typing import TYPE_CHECKING

from Functions.Network.Accounts.AccountAuthentication.Server.PreAuthAccount import PreAccount
from Functions.Network.SecurityInfo import SecurityInfo
from Functions.logManager import Logs

if TYPE_CHECKING:
    from Functions.Network.Accounts.AccountAuthentication.Server.ServerAuthentication import Authentication as Auth


def _PhaseVerification(logs: Logs, data: dict, account: PreAccount, Authentication: 'Auth') -> bool:

    # Rule 1
    if len(data['nickname']) > 30 or len(data['nickname']) < 3:
        account.socket.send(Authentication._fillText("Nickname must be between 3 and 30 symbols.",
                                                     SecurityInfo.preAuthMessageLength).encode())
        logs.sendLog(f"[Authentication] Couldn't pass authentication verification phase. "
                     f"{account.socket.getpeername()[0]}:{account.socket.getpeername()[1]}", -1)
        account.socket.close()
        return False

    # Rule 2
    if data['nickname'].lstrip(' ').rstrip(' ').replace('  ', ' ') != data['nickname']:
        account.socket.send(Authentication._fillText("Space rules violation.",
                                                     SecurityInfo.preAuthMessageLength).encode())
        logs.sendLog(f"[Authentication] Couldn't pass authentication verification phase. "
                     f"{account.socket.getpeername()[0]}:{account.socket.getpeername()[1]}", -1)
        account.socket.close()

    # Rule 3
    if len(data['pc_name']) > 50 or len(data['pc_name']) < 2:
        account.socket.send(Authentication._fillText("PC name must be between 2 and 50 symbols.",
                                                     SecurityInfo.preAuthMessageLength).encode())
        logs.sendLog(f"[Authentication] Couldn't pass authentication verification phase. "
                     f"{account.socket.getpeername()[0]}:{account.socket.getpeername()[1]}", -1)
        account.socket.close()
        return False
    logs.sendLog("[Authentication] Verification phase has been passed." +
                 f"{account.socket.getpeername()[0]}:{account.socket.getpeername()[1]}", -1)
    return True
