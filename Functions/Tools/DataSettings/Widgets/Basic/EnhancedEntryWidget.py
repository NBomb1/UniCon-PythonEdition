from Functions.Tools.DataSettings.Widgets.Basic.SaveWidgetData import SaveWidgetData
from UI.TKinter_addons.Entry_Placeholder import EntryWithPlaceholder
import tkinter as tk


class EnhancedEntry(EntryWithPlaceholder, SaveWidgetData):
    """
    Uses for Settings Menu.
    Its Entry itself.
    """
    def __init__(
            self,
            master: tk.Widget = None,
            placeholder: str = "PLACEHOLDER",
            color: str = 'grey',
            maxLen: int = 80,
            minLen: int = 3,
            symbolExceptions=None,
            checkFunc=None,
    ):
        if checkFunc is None:
            checkFunc = []
        if symbolExceptions is None:
            symbolExceptions = []

        self.actualData = ''
        self.maxLen = maxLen
        self.minLen = minLen
        self.symbolExceptions = symbolExceptions
        self.checkFunc = checkFunc

        super().__init__(master, placeholder, color)

        self._var = tk.StringVar()
        self.configure(textvariable=self._var)

    def save(self) -> list[str]:
        """
        :return: list of refuse reasons.
        """
        res = self.checkCorrectness()
        if len(res):
            self.actualData = self._var.get()
        if self.dataSaver is not None:
            self.dataSaver(self.actualData)
        return res

    def checkCorrectness(self) -> list[str]:
        checkAll = [
            self.maxLenCheck,
            self.minLenCheck,
            self.checkCorrectness
        ]
        checkAll.extend(self.checkFunc)
        for i in range(len(checkAll)):
            checkAll[i] = checkAll[i](self._var.get())

        checkAll = list(filter(lambda x: x != '', checkAll))
        return checkAll

    def maxLenCheck(self) -> str:
        return '' if len(self._var.get()) <= self.maxLen else 'Too big size'

    def minLenCheck(self) -> str:
        return '' if len(self._var.get()) >= self.minLen else 'Too low size'

    def exceptionCheck(self) -> str:
        return '' if self._var.get() not in self.symbolExceptions else 'Restricted value'
