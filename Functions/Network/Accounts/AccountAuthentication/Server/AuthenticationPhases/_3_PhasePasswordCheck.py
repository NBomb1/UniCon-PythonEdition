import hashlib
import socket
from time import sleep

from Functions.Network.SecurityInfo import SecurityInfo
from Functions.logManager import Logs

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from Functions.Network.Accounts.AccountAuthentication.Server.ServerAuthentication import Authentication as Auth


def _3_PhasePasswordCheck(s: socket.socket, password: str, logs: Logs, client_salt: bytes, Authentication: 'Auth') -> bool:
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
