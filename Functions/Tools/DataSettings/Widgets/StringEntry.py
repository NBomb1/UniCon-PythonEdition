import tk

from Functions.Tools.DataSettings.Widgets.Basic.EnhancedEntryWidget import EnhancedEntry


class StringEntry(EnhancedEntry):
    def __init__(
            self,
            master: tk.Widget = None,
            placeholder: str = "PLACEHOLDER",
            color: str = 'grey',
            maxLen: int = 80,
            minLen: int = 3,
            symbolExceptions: list[str] = None,
            checkFunc: list[callable] = None
    ):
        super().__init__(master, placeholder, color, maxLen, minLen, symbolExceptions, checkFunc)

    def get(self) -> str:
        return self.actualData

    def getCurrent(self) -> str:
        return self._var.get()
