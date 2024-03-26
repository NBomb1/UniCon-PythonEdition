from time import sleep

from Functions.Tools.DataSettings.Widgets.Basic.SaveWidgetData import SaveWidgetData
from Functions.Tools.DataSettings.Widgets.Basic.ShowRedFlag import ShowRedFlag
from Functions.Tools.DataSettings.Widgets.Basic.ToolTip import ToolTip
from UI.TKinter_addons.Entry_Placeholder import EntryWithPlaceholder
import tkinter as tk


class EnhancedEntry(EntryWithPlaceholder, SaveWidgetData, ShowRedFlag):
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

        self.ToolTip = ToolTip(self, '')

        self._var = tk.StringVar()
        self.configure(textvariable=self._var)

        # self._foc_out()
        self._loadFunc(self.load)

        self._put_placeholder()

    def load(self, data: str):
        self.actualData = data
        self._foc_in()
        self.delete("0", tk.END)
        self.insert("1", str(data))
        self._foc_out()

    def save(self) -> list[str]:
        """
        :return: list of refuse reasons.
        """
        res = []
        if self.get() == self.placeholder and self.cget('fg') == self.placeholder_color:
            res.append('No data given', )
        else:
            res.extend(self.checkCorrectness())

        if not len(res):
            self.actualData = self._var.get()
            if self.dataSaver is not None:
                self.dataSaver(self.actualData)
            self.showFlag(self, 'green')
        else:
            self.showFlag(self)
            self.bell()
        self.ToolTip.change_text('\n'.join(res))
        return res

    def checkCorrectness(self) -> list[str]:
        checkAll = [
            self.maxLenCheck,
            self.minLenCheck,
            self.exceptionCheck
        ]
        checkAll.extend(self.checkFunc)
        for i in range(len(checkAll)):
            checkAll[i] = checkAll[i](self._var.get())

        checkAll = list(filter(lambda x: x != '', checkAll))
        return checkAll

    def maxLenCheck(self, string: str) -> str:
        return '' if len(string) <= self.maxLen else 'Too big size'

    def minLenCheck(self, string: str) -> str:
        return '' if len(string) >= self.minLen else 'Too low size'

    def exceptionCheck(self, string: str) -> str:
        return '' if string not in self.symbolExceptions else 'Restricted value'
