import tkinter as tk
from threading import Thread
from time import sleep

import settings


class ShowRedFlag:
    @staticmethod
    # bgAfterChange='#FF2B2A'
    # fgAfterChange='white'
    #         bgAfterChange=None,
    #         fgAfterChange=None
    def showFlag(
            widget: tk.Widget,
            bgWhileChange='#FF2B2A',
            fgWhileChange='white',
            bgAfterChange=None,
            fgAfterChange=None
    ):
        ShowRedFlag.disableFocus(widget, True)
        bgOrigin = widget.cget('bg') if bgAfterChange is None else bgAfterChange
        fgOrigin = widget.cget('fg') if fgAfterChange is None else fgAfterChange

        widget.configure(bg=bgWhileChange)
        widget.configure(fg=fgWhileChange)

        def func():
            sleep(settings.SettingsMenu.widgetsWait)
            widget.configure(bg=bgOrigin)
            widget.configure(fg=fgOrigin)
            ShowRedFlag.disableFocus(widget, False)
        Thread(target=func, daemon=True).start()

    @staticmethod
    def disableFocus(widget: tk.Widget, mode: bool):
        func = getattr(widget, 'disableFocus')
        if func is not None:
            func(mode)
