import tk as tk

from Functions.Tools.DataSettings.Widgets.Basic.EnhancedEntryWidget import EnhancedEntry


class IntegerEntry(EnhancedEntry):
    def __init__(
            self,
            master: tk.Widget = None,
            placeholder: str = "PLACEHOLDER",
            color: str = 'grey',
            maxLen: int = 80,
            minLen: int = 3,
            symbolExceptions: list[str] = None,
            checkFunc: list[callable] = None,
            from_: int | None = None,
            to_: int | None = None
    ):
        self.from_ = from_
        self.to_ = to_
        checkFunc.append(self._numberCheck)

        super().__init__(master, placeholder, color, maxLen, minLen, symbolExceptions, checkFunc)

    def get(self) -> int:
        return int(self.actualData)

    def getCurrent(self) -> str:
        return self._var.get()

    def _numberCheck(self):
        if not self._var.get().isnumeric():
            return 'Is not number'
        if self.to_ > int(self._var):
            return 'Too big number'
        if self.from_ > int(self._var):
            return 'Too small number'
        return ''
