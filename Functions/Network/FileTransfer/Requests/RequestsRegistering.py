from functools import partial
from hashlib import sha256
from os import urandom
from typing import TYPE_CHECKING

from Functions.Network.Accounts.AccountData import Account
from Functions.Network.Accounts.AccountManager import AccountManager
from Functions.Network.FileTransfer.Data.States import RequestStates
from Functions.Network.FileTransfer.Files.Receiving.FileReceivingContainer import ReceivingContainer
from Functions.Network.FileTransfer.Files.Sending.FileSendingContainer import SendingInfo
from Functions.Network.FileTransfer.Requests.ClientToClient import ClientToClient
from Functions.Network.FileTransfer.Requests.SelfReceiver import SelfReceiver
from Functions.Network.FileTransfer.Requests.SelfSender import SelfSender
from Functions.logManager import Logs

if TYPE_CHECKING:
    from Functions.Network.FileTransfer.FileTransfer import FileTransfer


class RequestRegistering(RequestStates):
    all_requests: dict[bytes, SelfSender | SelfReceiver | ClientToClient] = {}

    accountManager: AccountManager
    logs: Logs
    fileTransfer: 'FileTransfer'
    on_request_update: callable

    def _registerSelfSenderRequest(self, receiver: Account, file_container: SendingInfo, moduleID: str) -> SelfSender:
        assert self.fileTransfer.is_enabled.savedData, "Can't send files while file transferring is restricted."

        while True:
            code = sha256(urandom(128)).hexdigest().encode()
            if code not in self.all_requests:
                break
        request = SelfSender(
            receiver,
            self.accountManager,
            self.logs,
            file_container,
            code,
            moduleID,
            partial(self.on_request_update, code)
        )

        if self.accountManager.getIsServer():
            request.updateState(self.state_serverAccepted)
        request.invite()

        self.all_requests[code] = request

        self.checking_requests()

        # calling function when request is created
        for function in self.fileTransfer.trigger_requestAdded:
            function(request)
        return request

    def __registerSelfReceivingRequest(self, receiver: Account, file_container: ReceivingContainer, moduleID: str,
                                       code: bytes) -> SelfReceiver:
        assert self.fileTransfer.is_enabled.savedData, "Can't receive files while file transferring is restricted."
        self.on_request_update()

        request = SelfReceiver(
            receiver,
            self.accountManager,
            self.logs,
            file_container,
            code,
            moduleID,
            partial(self.on_request_update, code)
        )

        request.updateState(self.state_serverAccepted)

        self.all_requests[code] = request

        self.checking_requests()
        return request

    def checking_requests(self):
        print(
            f"""------Checking-requests-info--------\n\n"""
            f"""=============Count==================\n"""
            f"""All requests: {len(self.all_requests)}\n"""
            f"""Sending requests: {len(tuple(filter(
                lambda x: isinstance(x, SelfSender),
                self.all_requests
            )))}\n"""
            f"""Receiving requests: {len(tuple(filter(
                lambda x: isinstance(x, SelfReceiver),
                self.all_requests
            )))}\n"""
            f"""Other requests: {len(tuple(filter(
                lambda x: isinstance(x, ClientToClient),
                self.all_requests
            )))}\n"""
            f"""=====================================\n\n"""
            f"""================Info================\n"""
        )
        for i in range(len(self.all_requests)):
            request: SelfSender = tuple(self.all_requests.values())[i]
            print(
                f"""{i + 1}. {type(request).__name__}\n"""
                f"""Sender: {request.sender}\n"""
                f"""Receiver: {request.receiver}\n"""
                f"""States: {request.getHistoryStates_str()}\n"""
                f"""Code: {request.code}\n"""
                f"""Files: {request.file_container.sending_information_format()}\n\n\n"""
            )
