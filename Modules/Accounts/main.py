from Functions.ModuleHandler.moduleAPI import API
from Functions.Network.Accounts.AccountData import Account
from Functions.Network.MainChannel.Client.MainChannel import ClientMainChannel
from Functions.Network.MainChannel.Server.main import ServerMainChannel
from Functions.Tools.ScrollableFrame import ScrollableFrame
import tkinter as tk

from Modules.Accounts.Design.AccountLeftSideInfo import LeftSideInfo
from Modules.Accounts.Design.AccountRightSIdeInfo import RightSideInfo


class Module(RightSideInfo):
    id_ = "Qzc2rFEcJf0s3&d#qj1kC$A7P!~lG}tUu9vWb4xLh5KgZiope^mD(R)=O*wyXT6B"
    version = "0.0.1"
    name = "Accounts"
    author = "ArT"
    defaultNetworkAuth = True
    isOnlyUI = True
    allAccounts: dict[Account, LeftSideInfo] = {}

    def __init__(self, api: API):
        self.api = api
        self.notebook = self.api.getRightNotebook()
        self.triggerManager = self.api.getTriggerManager()

        self.frame = tk.Frame(self.api.getRightNotebook())
        self.frameDisabled = tk.Frame(self.frame)
        self.frameEnabled = tk.Frame(self.frame)

        self.notebook.add(self.frame, text='Accounts', state=tk.DISABLED)

        self.setup()
        self.frameDisabled.pack()

        self.notebook.tab(self.frame, state=tk.NORMAL)

        # Setting triggers
        self.triggerManager.accountAddedTrigger(self.createNewAccount)  # started as server
        self.triggerManager.serverStartedTrigger(self.serverStarted)  # started as client
        # self.triggerManager.clientConnectedTrigger(self.clientConnected)  # client connected
        self.triggerManager.clientConnectedTrigger(self.serverStarted)  # client connected
        self.triggerManager.accountRemovedTrigger(self.clientDisconnected)  # client disconnected
        # self.triggerManager.accountRemovedTrigger(self.clientDisconnected)  # client disconnected

    def setup(self):
        self.labelServerNotActive = tk.Label(self.frameDisabled,
                                             text='Connect or create the server to see account info.',
                                             font=(None, 10, 'bold')
                                             )
        self.labelServerNotActive.pack(anchor=tk.CENTER, expand=True)
        self.accountListFrame = ScrollableFrame(self.frameEnabled)

        self.accountInformationFrame = ScrollableFrame(self.frameEnabled)
        self.accountListFrame.pack(side=tk.LEFT, fill=tk.Y)
        self.accountInformationFrame.pack(expand=True, fill=tk.BOTH)
        self.accountListFrame.canvas.configure(width=200)

        self.accountListFrame.inner_frame.configure(bg='#B5B5B5')
        self.accountInformationFrame.inner_frame.configure(bg='red')
        self.createWidgets(self.accountInformationFrame.inner_frame)

    def createNewAccount(self, account: Account):
        self.allAccounts[account] = LeftSideInfo(self.accountListFrame.inner_frame, account, self.show)
        if isinstance(account, Account):
            account.add_on_ping_update_function(self.pingUpdated)

    def serverStarted(self, serverInfo: ServerMainChannel):
        self.createNewAccount(serverInfo.accountManager.getSelfAccount())
        self.frameDisabled.pack_forget()
        self.frameEnabled.pack(fill=tk.BOTH, expand=True)

    # def clientConnected(self, serverInfo: ClientMainChannel):
    #     self.createNewAccount(serverInfo.accountManager.getSelfAccount())

    def pingUpdated(self, account: Account):
        self.allAccounts[account].updateInfo()

    def clientDisconnected(self, account: Account):
        self.allAccounts.get(account).mainFrame.destroy()
