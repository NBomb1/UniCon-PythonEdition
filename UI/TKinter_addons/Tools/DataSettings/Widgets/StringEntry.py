import tkinter as tk

from UI.TKinter_addons.Tools.DataSettings.Widgets.Basic.EnhancedEntryWidget import EnhancedEntry


class StringEntry(EnhancedEntry):
    def __init__(
            self,
            master: tk.Widget = None,
            placeholder: str = "PLACEHOLDER",
            color: str = 'grey',
            maxLen: int = 80,
            minLen: int = 3,
            symbolExceptions: list[str] = None,
            checkFunc: list[callable] = None,
            default=None
    ):
        super().__init__(master, placeholder, color, maxLen, minLen, symbolExceptions, checkFunc, default)

    def getData(self) -> str:
        return self.actualData

    def getCurrent(self) -> str:
        return self._var.get()
