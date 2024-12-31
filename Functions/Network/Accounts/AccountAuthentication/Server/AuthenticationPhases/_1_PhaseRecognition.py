from Functions.Network.Accounts.AccountAuthentication.Server.PreAuthAccount import PreAccount
from Functions.Network.ModuleConnector.ConnectorManager import ConnectorManager
from Functions.Network.SecurityInfo import SecurityInfo
from Functions.logManager import Logs

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Functions.Network.FileTransfer.FileTransfer import FileTransfer
    from Functions.Network.Accounts.AccountAuthentication.Server.ServerAuthentication import Authentication as Auth


def _1_PhaseRecognition(
        account: PreAccount,
        mcm: ConnectorManager,
        logs: Logs,
        Authentication: 'Auth',
        fileTransfer: 'FileTransfer'
) -> bool | None:
    """Phase 1 - Recognition: We do not accept connections from others programs."""
    message = Authentication._getMessage(account.socket)
    if message is None:
        account.socket.close()
        return True
    message = message.replace(' ', '')  # formatting to built-in len default

    # checking if code is the same
    if message == SecurityInfo.unique_message:
        logs.sendLog("[Authentication] First phase has been passed."
                     f"{account.socket.getpeername()[0]}:{account.socket.getpeername()[1]}", -1)
        return False
    elif fileTransfer.requestsHandler.check_special_code(message, account.socket):
        return True
    elif mcm.server.checkSpecialCode(message, account.socket):
        return True
    else:
        account.socket.send(
            Authentication._fillText("!!Connection restriction", SecurityInfo.preAuthMessageLength).encode())
        logs.sendLog(f"[Authentication] Couldn't pass 1st authentication phase. "
                     f"{account.socket.getpeername()[0]}:{account.socket.getpeername()[1]}", -1)
        account.socket.close()
        return True
