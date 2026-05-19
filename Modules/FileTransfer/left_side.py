import tkinter as tk
from threading import Thread
from time import sleep

from Functions.Network.FileTransfer.Requests.ClientToClient import ClientToClient
from Functions.Network.FileTransfer.Requests.SelfReceiver import SelfReceiver
from Functions.Network.FileTransfer.Requests.SelfSender import SelfSender
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from Modules.FileTransfer.main import Module


class LeftSide(tk.Frame):
    def __init__(
            self,
            root: tk.Frame,
            fileTransfer: 'Module'
    ):
        super().__init__(root)
        self.fileTransfer = fileTransfer

        self.root = root
        self.request: SelfReceiver | SelfSender | ClientToClient | None = None

        self.label_type = tk.Label(self)
        self.label_sender = tk.Label(self)
        self.label_receiver = tk.Label(self)
        self.label_status = tk.Label(self)

        self.label_type.pack()
        self.label_sender.pack()
        self.label_receiver.pack()
        self.label_status.pack()

        self.bind("<Enter>", self.on_enter)
        self.bind("<Leave>", self.on_leave)

        self.bind("<Button-1>", self.on_click)
        self.label_type.bind("<Button-1>", self.on_click)
        self.label_sender.bind("<Button-1>", self.on_click)
        self.label_receiver.bind("<Button-1>", self.on_click)
        self.label_status.bind("<Button-1>", self.on_click)

        self.pack(fill=tk.X, expand=True, padx=1, pady=(0, 3))
        Thread(target=self.update_cycle, daemon=True).start()

    def set_obj(self, object_: SelfReceiver | SelfSender | ClientToClient):
        assert isinstance(object_, (SelfReceiver, SelfSender, ClientToClient)), 'Wrong type'
        self.request = object_
        self.update_data()

    def update_data(self) -> None:
        assert self.request is not None, "Object can't be None."
        self.label_type.configure(
            text='Sender type' if isinstance(self.request, SelfSender) else
            'Receiver type' if isinstance(self.request, SelfReceiver) else
            'ClientToClient type'
        )

        self.label_sender.configure(text=f"S.: {self.request.sender.nickname}")
        self.label_receiver.configure(text=f"R.: {self.request.receiver.nickname}")
        self.label_status.configure(text=f"{self.request.states_dict_int_to_str.get(self.request.getState())}")

    def disable(self):
        self.request = None
        self.pack_forget()

    def on_enter(self, event):
        event.widget.config(cursor="hand2")

    def on_leave(self, event):
        event.widget.config(cursor="")

    def update_cycle(self):
        while True:
            sleep(0.5)
            if self.request:
                self.update_data()

    def on_click(self, x=None):
        self.fileTransfer.right_side_info.show(self.request)
