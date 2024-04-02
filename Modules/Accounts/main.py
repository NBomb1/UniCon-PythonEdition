from Functions.ModuleHandler.moduleAPI import API
from Functions.Network.Accounts.AccountData import Account
from Functions.Network.MainChannel.Client.MainChannel import ClientMainChannel
from Functions.Network.MainChannel.Server.main import ServerMainChannel
from Functions.Tools.ScrollableFrame import ScrollableFrame
import tkinter as tk

from Modules.Accounts.Design.AccountLeftSideInfo import LeftSideInfo


class Module:
    version = "0.0.1"
    name = "Accounts"
    author = "ArT"
    defaultNetworkAuth = True
    isOnlyUI = True

    def __init__(self, api: API):
        self.api = api
        self.notebook = self.api.getRightNotebook()
        self.triggerManager = self.api.getTriggerManager()

        self.frame = tk.Frame(self.api.getRightNotebook())

        self.notebook.add(self.frame, text='Accounts', state=tk.DISABLED)

        self.setup()

        self.notebook.tab(self.frame, state=tk.NORMAL)
        self.triggerManager.accountAddedTrigger(self.createNewAccount)
        self.triggerManager.serverStartedTrigger(self.serverStarted)
        self.triggerManager.clientConnectedTrigger(self.clientConnected)

    def setup(self):
        self.accountListFrame = ScrollableFrame(self.frame)

        self.accountInformationFrame = ScrollableFrame(self.frame)
        self.accountListFrame.pack(side=tk.LEFT, fill=tk.Y)
        self.accountInformationFrame.pack(expand=True, fill=tk.BOTH)
        self.accountListFrame.canvas.configure(width=200)

        self.accountListFrame.inner_frame.configure(bg='#B5B5B5')
        self.accountInformationFrame.inner_frame.configure(bg='red')

    def createNewAccount(self, account: Account):
        LeftSideInfo(self.accountListFrame.inner_frame, account)

    def serverStarted(self, serverInfo: ServerMainChannel):
        self.createNewAccount(serverInfo.accountManager.getSelfAccount())

    def clientConnected(self, serverInfo: ClientMainChannel):
        self.createNewAccount(serverInfo.account.getSelfAccount())
