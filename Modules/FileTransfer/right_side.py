import datetime
import tkinter as tk
import tkinter.ttk as ttk
from threading import Thread
from time import sleep

from Functions.Network.FileTransfer.Requests.ClientToClient import ClientToClient
from Functions.Network.FileTransfer.Requests.SelfReceiver import SelfReceiver
from Functions.Network.FileTransfer.Requests.SelfSender import SelfSender
from UI.TKinter_addons.Tools.ScrollableFrame import ScrollableFrame


class RightSide(ScrollableFrame):
    def __init__(self, root: tk.Frame):
        super().__init__(root)
        self.root = root

        self.current = None

        self.label_type = tk.Label(self.inner_frame)

        # left side
        self.label_sender_left = tk.Label(self.inner_frame, text='Sender:')
        self.label_receiver_left = tk.Label(self.inner_frame, text='Receiver:')
        self.label_current_state_left = tk.Label(self.inner_frame, text='Current state:')
        self.label_all_files_left = tk.Label(self.inner_frame, text='Files:')

        # Right side
        self.label_sender = tk.Label(self.inner_frame, anchor=tk.E)
        self.label_receiver = tk.Label(self.inner_frame, anchor=tk.E)
        self.label_current_state = tk.Label(self.inner_frame, anchor=tk.E)
        self.label_all_files = tk.Label(self.inner_frame, anchor=tk.E)

        # Bottom side
        self.current_file = tk.Label(self.inner_frame)
        self.progressbar_certain = ttk.Progressbar(self.inner_frame)
        self.progressbar_global = ttk.Progressbar(self.inner_frame)

        self.label_states_history = tk.Label(self.inner_frame, anchor=tk.E)

        self.inner_frame.grid_columnconfigure(1, weight=True)

        # Placing widgets
        self.label_type.grid(columnspan=2, row=0)
        self.label_sender_left.grid(column=0, row=1, sticky=tk.W)
        self.label_receiver_left.grid(column=0, row=2, sticky=tk.W)
        self.label_current_state_left.grid(column=0, row=3, sticky=tk.W)
        self.label_all_files_left.grid(column=0, row=4, sticky=tk.W)

        self.label_sender.grid(column=1, row=1, sticky=tk.E)
        self.label_receiver.grid(column=1, row=2, sticky=tk.E)
        self.label_current_state.grid(column=1, row=3, sticky=tk.E)
        self.label_all_files.grid(column=1, row=4, sticky=tk.E)

        self.current_file.grid(row=5, columnspan=2)
        self.progressbar_certain.grid(row=6, columnspan=2, sticky=tk.W + tk.E)
        self.progressbar_global.grid(row=7, columnspan=2, sticky=tk.W + tk.E)
        self.label_states_history.grid(row=8, columnspan=2)
        # self.label_states_history.grid(row=7, columnspan=2)

        Thread(target=self.update_cycle, daemon=True).start()

    def show(self, request: SelfReceiver | SelfSender | ClientToClient = None):
        if self.current == request:
            self.pack_forget()
            self.current = None
            return
        else:
            self.grid(sticky=tk.NSEW, column=2, row=1)
            self.update_data(request)

    def update_data(self, request: SelfReceiver | SelfSender | ClientToClient = None):
        self.current = request if request is not None else self.current
        assert self.current is not None

        # Right side
        self.label_type.configure(
            text='Sender type' if isinstance(self.current, SelfSender) else
            'Receiver type' if isinstance(self.current, SelfReceiver) else
            'ClientToClient type'
        )
        self.label_sender.configure(text=self.current.sender)
        self.label_receiver.configure(text=self.current.receiver)
        self.label_current_state.configure(text=self.current.states_dict_int_to_str.get(self.current.getState()))
        self.label_all_files.configure(text=self.current.file_container.sending_information_format().__str__())

        # Bottom side
        self.current_file.configure(
            text=f'File: {self.current.current.name}' if not isinstance(self.current.current, int) else 'Unknown'
        )
        self.progressbar_certain.configure(
            value=self.current.current.progress if not isinstance(self.current.current, int) else self.current.current,
            maximum=1
        )
        self.progressbar_global.configure(
            value=self.current.file_container.calculate_bytes_sent() / self.current.file_container.calculate_bytes(),
            maximum=1
        )

        states = ''
        history = self.current.getHistoryStates_str()
        for i in history.keys():
            states += f'{datetime.datetime.fromtimestamp(i).__str__().replace("-", ".").replace(" ", " - ")} - ' \
                      f'{history.get(i)}\n'
        self.label_states_history.configure(
            text=f'All states: \n{states[:-1]}'
        )

    def update_cycle(self):
        while True:
            sleep(0.05)
            if self.current:
                self.update_data()
