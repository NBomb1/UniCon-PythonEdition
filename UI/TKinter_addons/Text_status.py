import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from datetime import datetime


class StatusText(ScrolledText):
    def __init__(self, master):
        super().__init__(master)
        # Creating ping text color
        # latency below 81 ms
        self.tag_configure("ping-good", background="green", foreground='white')
        # latency from 81 to 250
        self.tag_configure("ping-middle", background="yellow", foreground='black')
        # latency from 251 to 500
        self.tag_configure("ping-poor", background="dark orange", foreground='white')
        # latency starts at 501
        self.tag_configure("ping-worst", background="red", foreground='white')

        # statuses
        self.tag_configure("status-online", foreground='GreenYellow')
        self.tag_configure("status-offline", foreground='white', background='black')
        self.tag_configure("status-connected", foreground='green')
        self.tag_configure("status-disconnected", foreground='red')  # shows for 5 sec
        self.tag_configure("status-reconnecting", foreground='white', background='red')
        self.tag_configure("status-hosting", foreground='aquamarine')

        # modes
        self.tag_configure("mode-mode is not chosen")  # default
        self.tag_configure("mode-client", foreground='white', background='goldenrod')
        self.tag_configure("mode-host", foreground='white', background='black')

        # disabling user text changing
        self.configure(state=tk.DISABLED)

    def create_status(self, mode: str, status: str, ping: int | str | None):
        # checking typos
        assert mode in ['mode is not chosen', 'client', 'host']
        assert status in ['online', 'offline', 'connected', 'disconnected', 'reconnecting', 'hosting']

        # preparation
        self.configure(state=tk.NORMAL)
        index = len(self.get('1.0', tk.END)) - len(self.get('1.0', tk.END).replace('\n', ''))

        # baking text
        text = f"You are - {mode}\n" \
               f"Status: {status}"
        if status == 'connected':
            text += f'\nYour ping: {ping}'
        elif status == 'reconnecting':
            text += f'\nReconnecting in: {ping}' if isinstance(ping, int) else '\nReconnecting'
        elif status == 'disconnected':
            text += f' {ping}'

        # inserting text to widget
        self.insert(tk.END, text)

        # choosing colors

        # coloring
        self.tag_add('mode-' + mode, '1.10', '1.99')
        self.tag_add('status-' + status, '2.8', '2.99')
        if status == 'connected':
            quality = (
                'ping-good' if ping <= 80
                else 'ping-middle' if ping <= 250
                else 'ping-poor' if ping <= 500
                else 'ping-worst'
            )
            self.tag_add(quality, '3.11', '3.99')

        # disabling user changing
        self.configure(state=tk.DISABLED)
