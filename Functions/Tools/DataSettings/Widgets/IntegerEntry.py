import tkinter as tk

from Functions.Tools.DataSettings.Checks import checkInteger
from Functions.Tools.DataSettings.Widgets.Basic.EnhancedEntryWidget import EnhancedEntry


class IntegerEntry(EnhancedEntry):
    def __init__(
            self,
            master: tk.Widget = None,
            placeholder: str = "PLACEHOLDER",
            color: str = 'grey',
            maxLen: int = 30,
            minLen: int = 1,
            symbolExceptions: list[str] = None,
            checkFunc: list[callable] = None,
            from_: int = -999999999999,
            to_: int = 999999999999
    ):
        checkFunc = [] if checkFunc is None else checkFunc
        self.from_ = from_
        self.to_ = to_
        checkFunc.append(self._numberCheck)

        super().__init__(master, placeholder, color, maxLen, minLen, symbolExceptions, checkFunc)

    def getData(self) -> int:
        return int(self.actualData)

    def getCurrent(self) -> str:
        return self._var.get()

    def _numberCheck(self, number: str):
        return 'Is not number' if not checkInteger(number) else \
               'Too big number' if self.to_ < int(number) else \
               'Too small number' if self.from_ > int(number) else ''
