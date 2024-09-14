import socket
from ast import literal_eval

from Functions.Network.SecurityInfo import SecurityInfo
from Functions.logManager import Logs

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Functions.Network.Accounts.AccountAuthentication.Server.ServerAuthentication import Authentication as Auth


def _2_PhaseBuiltInModuleCheck(s: socket.socket, logs: Logs, Authentication: 'Auth') -> bool:
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
        if i == 'UI':
            continue
        if modules[i] is not None and modules[i] != message[i]:  # if version is not the same
            send[i] = modules[i]  # adding version message

    if send:  # checking if there are any issues with module versions
        s.send(send.__str__().encode())  # sending our module versions
        logs.sendLog("[Authentication] Couldn't pass 2nd authentication phase."
                     f"{s.getpeername()[0]}:{s.getpeername()[1]}", -1)
        s.close()  # and closing connection
        return False

    logs.sendLog("[Authentication] Second phase has been passed."
                 f"{s.getpeername()[0]}:{s.getpeername()[1]}", -1)
    return True
