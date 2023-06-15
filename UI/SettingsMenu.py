import tkinter as tk

class Settings(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)

        # setting the window
        self.grab_set()
        self.wm_minsize(400, 300)
        self.title("Settings")
