import tkinter as tk
from UI.window.WidnowCenter import center_child


class Settings(tk.Toplevel):
    def __init__(self, master=None):
        super().__init__(master)

        # setting the window
        self.grab_set()
        self.wm_minsize(400, 300)
        self.title("Settings")
        center_child(self, master)
