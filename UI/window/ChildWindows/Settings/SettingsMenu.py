import tkinter as tk
import tkinter.ttk as ttk
from UI.window.WidnowCenter import center_child
import settings


class Settings(tk.Toplevel):
    def __init__(self, master: tk.Tk):
        super().__init__(master)

        # setting the window
        self.grab_set()
        self.wm_minsize(400, 300)
        self.title("Settings")
        center_child(self, master)

        self.labelframe_port = tk.LabelFrame(self, text='We can use ports')
        self.label_port_from = tk.Label(self.labelframe_port, text='from')
        self.label_spinbox_from = ttk.Spinbox(
            self.labelframe_port,
            from_=settings.MainMenu.port_from,
            to=settings.MainMenu.port_to
        )
        self.label_port_to = tk.Label(self.labelframe_port, text='to')
        self.label_spinbox_to = ttk.Spinbox(
            self.labelframe_port,
            from_=settings.MainMenu.port_from,
            to=settings.MainMenu.port_to,

        )
        self.label_spinbox_from.set(1025)
        self.label_spinbox_to.set(1225)

        self.labelframe_port.pack()
        self.label_port_from.pack()
        self.label_spinbox_from.pack()
        self.label_port_to.pack()
        self.label_spinbox_to.pack()

