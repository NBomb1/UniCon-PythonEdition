"""
This module shows account information and lets you manage them.
"""
from Functions.ModuleHandler.moduleAPI import API
from Functions.Network.Accounts.AccountData import Account
from Functions.Network.MainChannel.Server.main import ServerMainChannel
from UI.TKinter_addons.Tools.ScrollableFrame import ScrollableFrame
import tkinter as tk

from Modules.Accounts.Design.AccountLeftSideInfo import LeftSideInfo
from Modules.Accounts.Design.AccountRightSIdeInfo import RightSideInfo


class Module(RightSideInfo):
    """
    This class represents the AccountManager module. It manages user accounts and provides UI for managing them.

    Attributes:
    id_ (str): The unique identifier of the module.
    version (str): The version of the module.
    name (str): The name of the module.
    author (str): The author of the module.
    defaultNetworkAuth (bool): Whether the module requires network authentication by default.
    isUI (bool): Whether the module provides a user interface.
    allAccounts (dict[Account, LeftSideInfo]): A dictionary to store all accounts and their corresponding UI components.

    Methods:
    __init__(self, api: API): Initializes the module with the provided API instance.
    setup(): Sets up the UI components for the module.
    createNewAccount(self, account: Account): Creates a new account and its corresponding UI component.
    serverStarted(self, serverInfo: ServerMainChannel): Handles the server started event.
    pingUpdated(self, account: Account, what: str): Updates the UI component for a specific account.
    clientDisconnected(self, account: Account): Handles the client disconnected event.
    connectionClosed(): Handles the connection closed event.
    """
    id_ = "Qzc2rFEcJf0s3&d#qj1kC$A7P!~lG}tUu9vWb4xLh5KgZiope^mD(R)=O*wyXT6B"
    version = "0.0.1"
    name = "AccountManager"
    author = "ArT"
    defaultNetworkAuth = True
    isUI = True
    allAccounts: dict[Account, LeftSideInfo] = {}

    def __init__(self, api: API):
        self.api = api
        self.notebook = self.api.getRightNotebook()
        self.triggerManager = self.api.getTriggerManager()
        self.accountManager = self.api.getAccountManager()

        self.frame = tk.Frame(self.api.getRightNotebook())
        self.frameDisabled = tk.Frame(self.frame)
        self.frameEnabled = tk.Frame(self.frame)

        self.notebook.add(self.frame, text='Accounts', state=tk.DISABLED)

        self.labelServerNotActive = tk.Label(self.frameDisabled,
                                             text='Connect or create the server to see account info.',
                                             font=(None, 10, 'bold')
                                             )
        self.accountListFrame = ScrollableFrame(self.frameEnabled)
        self.accountInformationFrame = ScrollableFrame(self.frameEnabled)

        self.setup()
        self.frameDisabled.pack()

        self.notebook.tab(self.frame, state=tk.NORMAL)

        # Setting triggers
        self.triggerManager.accountAddedTrigger(self.createNewAccount)  # started as server
        self.triggerManager.serverStartedTrigger(self.serverStarted)  # started as client
        # self.triggerManager.clientConnectedTrigger(self.clientConnected)  # client connected

        self.triggerManager.clientConnectedTrigger(self.serverStarted)  # client connected
        self.triggerManager.accountRemovedTrigger(self.clientDisconnected)  # client disconnected

        self.api.getAccountManager().serverStoppedTrigger(self.connectionClosed)
        self.api.getAccountManager().clientStoppedTrigger(self.connectionClosed)
        # self.triggerManager.accountRemovedTrigger(self.clientDisconnected)  # client disconnected

    def setup(self):
        self.labelServerNotActive.pack(anchor=tk.CENTER, expand=True)

        self.accountListFrame.pack(side=tk.LEFT, fill=tk.Y)
        self.accountInformationFrame.pack(expand=True, fill=tk.BOTH)
        self.accountListFrame.canvas.configure(width=200)

        self.accountListFrame.inner_frame.configure(bg='#B5B5B5')
        self.createWidgets(self.accountInformationFrame.inner_frame)

    def createNewAccount(self, account: Account):
        self.allAccounts[account] = LeftSideInfo(self.accountListFrame.inner_frame, account, self.show)
        account.addUpdatedAccount(self.pingUpdated)

    def serverStarted(self, serverInfo: ServerMainChannel):
        self.createNewAccount(serverInfo.accountManager.getSelfAccount())
        self.frameDisabled.pack_forget()
        self.frameEnabled.pack(fill=tk.BOTH, expand=True)

    # def clientConnected(self, serverInfo: ClientMainChannel):
    #     self.createNewAccount(serverInfo.accountManager.getSelfAccount())

    def pingUpdated(self, account: Account, what: str):
        if (res := self.allAccounts.get(account)) is not None:
            res.updateInfo()

    def clientDisconnected(self, account: Account):
        # print('deleting', account)
        if (res := self.allAccounts.get(account)) is not None:
            res.destroy()
            self.allAccounts.pop(account)
            # del res.mainFrame

    def connectionClosed(self):
        for i in self.allAccounts.keys():
            self.allAccounts.get(i).destroy()
        self.allAccounts.clear()
        self.frameDisabled.pack()
        self.frameEnabled.pack_forget()
