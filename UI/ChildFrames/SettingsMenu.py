import tkinter as tk
import settings
import tkinter.ttk as ttk


class Settings(ttk.Notebook):
    def __init__(self, master: tk.Widget):
        super().__init__(master)

        self.settingsFrame = tk.Frame()
        self.add(self.settingsFrame, text="Main Settings")

        self.labelframe_port = tk.LabelFrame(self.settingsFrame, text='We can use ports')
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
        self.label_spinbox_to.set(settings.MainMenu.port_to)

        self.label_port_from.pack()
        self.label_spinbox_from.pack()
        self.label_port_to.pack()
        self.label_spinbox_to.pack()
        
        self.labelframe_port.pack(anchor=tk.CENTER, expand=True)
