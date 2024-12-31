from Functions.Network.FileTransfer.ClientHandler import ClientHandler
from Functions.Network.FileTransfer.Data.Actions import Actions
from Functions.logManager import Logs
from Functions.ModuleHandler.moduleAPI import API
from Functions.Network.Accounts.AccountDataManager import AccountManager
from Functions.Network.Accounts.AccountData import Account
from Functions.Network.FileTransfer.Data.States import RequestStates
from Functions.Network.FileTransfer.Files.Sending.FileSendingContainer import SendingInfo
from Functions.Network.FileTransfer.Requests.SelfSender import SelfSender
from Functions.Network.FileTransfer.ServerHandler import ServerHandler
from Functions.Network.MainChannel.Client.MainChannel import ClientMainChannel
from Functions.Network.MainChannel.Server.main import ServerMainChannel

from typing import TYPE_CHECKING

from UI.ChildFrames.Categories.FileTransferSettings import FileTransferSettings
from UI.TKinter_addons.Tools.DataSettings.Widgets.checkWidget import CheckButton

if TYPE_CHECKING:
    from UI.MainMenu import MainMenu


class FileTransfer(RequestStates):
    def __init__(self):
        self.accountManager: AccountManager | None = None
        self.api: None | API = None
        self.logs: None | Logs = None
        self.requestsHandler: None | ServerHandler = None

        self.__mainMenu: None | 'MainMenu' = None
        self.settings: None | FileTransferSettings = None

        self.is_enabled: None | CheckButton = None
        self.auto_receiving: None | CheckButton = None
        self.allowUnknownModules_serverSide: None | CheckButton = None
        self.allowUnknownModules: None | CheckButton = None

    def getApi(self, api: API) -> None:
        """Инициализация API и AccountManager."""
        self.api = api
        self.accountManager = api.getAccountManager()
        self.logs = self.api.getLogs()

        self.api.getTriggerManager().serverStartedTrigger(self.on_connection)  # when server starts
        self.api.getTriggerManager().clientConnectedTrigger(self.on_connection)  # when client connects

        self.__mainMenu = api.getMainMenu()
        self.settings = self.__mainMenu.settingsFrame.fileTransferSettings

        self.is_enabled: CheckButton = self.settings.checkButton_allowFileTransfer
        self.auto_receiving: CheckButton = self.settings.checkButton_autoFileReceiving
        self.allowUnknownModules_serverSide: CheckButton = \
            self.settings.checkButton_allowFileSendingFromUnknownModules_serverSide
        self.allowUnknownModules: CheckButton = \
            self.settings.checkButton_allowFileSendingFromUnknownModules

    def create(self, moduleID: str, files: list[str], to: Account) -> SelfSender:
        """
        Создание запроса на отправку файла.
        """
        # 1.1 Checking connection
        assert self.accountManager.getIsServer() is not None, "Can't send files without connection."

        # 1.2 Checking account existence
        assert to in self.accountManager.getParticipants(), "Can't send files to non-existing account."

        sender = self.accountManager.getSelfAccount()
        assert sender is not None, "Sender can't be None."

        activeModule = self.api.getModuleLoader().findById(moduleID)
        assert activeModule is not None, "Module can't be None."

        files = SendingInfo(files)

        return self.requestsHandler._registerSelfSenderRequest(to, files, moduleID)  # _ is ok

    # IS NOT FINISHED YET
    def _main_response_handler(self, msg):
        assert self.requestsHandler is not None, "Can't be None"
        self.logs.sendLog(f"Got message: {msg}", -3)
        msg['action'] = Actions.actions_dict_int_to_str.get(msg['action'])
        msg['state'] = RequestStates.states_dict_int_to_str.get(msg['state'])
        print(f"Got message: {msg}")  # TODO: DELETE IT
        msg['action'] = Actions.actions_dict_str_to_int.get(msg['action'])
        msg['state'] = RequestStates.states_dict_str_to_int.get(msg['state'])

        if isinstance(self.requestsHandler, ServerHandler):  # if a server
            self.requestsHandler.checking_file_transfer_type(msg)
        else:
            self.requestsHandler.checking_file_transfer_type(msg)
        print('Finished processing message')

    def on_connection(self, item: ServerMainChannel | ClientMainChannel):
        if isinstance(item, ServerMainChannel):
            self.requestsHandler = ServerHandler(
                self.logs,
                self
            )
            self.accountManager.addNewAccountFunction(
                lambda x: x.socket.registerFunction(
                    'FileTransfer',
                    self._main_response_handler
                )
            )
        else:
            self.requestsHandler = ClientHandler(self.accountManager, self.logs, self)

            self.accountManager.getOwner().socket.registerFunction(
                'FileTransfer', self._main_response_handler
            )
