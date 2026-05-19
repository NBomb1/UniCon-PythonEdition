"""
Allows participants send their files and see information.
"""
import tkinter as tk

from Functions.ModuleHandler.moduleAPI import API
from Functions.Network.FileTransfer.Requests.ClientToClient import ClientToClient
from Functions.Network.FileTransfer.Requests.SelfReceiver import SelfReceiver
from Functions.Network.FileTransfer.Requests.SelfSender import SelfSender
from Modules.FileTransfer.left_side import LeftSide
from Modules.FileTransfer.right_side import RightSide
from UI.TKinter_addons.Tools.ScrollableFrame import ScrollableFrame


class Module:
    id_ = "Ty??;#dM:5aczRDHa9kNDd2$MwbJn?!_{0T9CtJuW@b!Y№BZtUjpNzejIT5#om%&"
    version = "0.0.1"
    name = "FileTransfer"
    author = "ArT"
    defaultNetworkAuth = True
    isUI = True

    def __init__(self, api: API):
        self.api = api
        self.logs = api.getLogs()
        self.file_transfer = self.api.getFileTransfer()
        self.accountManager = self.api.getAccountManager()
        self.triggerManager = self.api.getTriggerManager()

        self.frame_list: list[LeftSide] = []

        # setup
        notebook = self.api.getRightNotebook()
        self.frame = tk.Frame(notebook)
        notebook.add(self.frame, text='File Transfer')

        # Creating widgets
        self.button_send_files = tk.Button(self.frame)
        self.scrollableFrameList = ScrollableFrame(self.frame)
        self.right_side_info = RightSide(self.frame)

        # Placing widgets
        # self.button_send_files.grid(column=0, row=0, sticky=tk.E + tk.W)  # i didn't check how it looks
        self.scrollableFrameList.grid(column=0, row=1)

        self.scrollableFrameList.canvas.configure(width=200)
        self.scrollableFrameList.inner_frame.configure(bg='#B5B5B5')

        self.file_transfer.request_added_Trigger(self.request_added)
        self.file_transfer.request_removed_Trigger(self.request_removed)

    def request_added(self, request: SelfReceiver | SelfSender | ClientToClient):
        # Because tkinter saves deleted widgets
        checking_list = tuple(filter(lambda x: x.request is None, self.frame_list))
        if checking_list:
            frame = checking_list[0]
        else:
            frame = LeftSide(self.scrollableFrameList.inner_frame, self)
        frame.set_obj(request)

        self.frame_list.append(frame)

    def request_removed(self, request: SelfReceiver | SelfSender | ClientToClient):
        for i in self.frame_list:
            if i.request is request:
                i.disable()
