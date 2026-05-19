import tkinter as tk


class InteractionFrame(tk.Frame):
    def __init__(self, master: tk.Widget):
        super().__init__(master)
        self.is_showing_request = False



