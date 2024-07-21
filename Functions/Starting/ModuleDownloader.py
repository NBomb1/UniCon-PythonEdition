import os
import sys

from Functions.Starting.ModuleChecker import *
from Functions.Starting.MissingModule import MissingModule
import tkinter as tk

from UI.window.WindowCenter import center_main


class CheckModules:
    """
    This class is responsible for checking if required modules are installed and displaying a warning if not.
    It also initializes the main window and sets up the GUI components.

    Attributes:
    textFont: A tuple representing the font style for GUI components.

    Methods:
    __init__(): Initializes the class and sets up the necessary attributes.
    showWarning(): Displays a warning message and GUI components if required modules are not installed.
    """
    textFont = (None, 15, 'bold')

    def __init__(self):
        """
        Initializes the CheckModules class.

        This method sets up the necessary attributes for the CheckModules class. It calculates the absolute path to the main
        script file, initializes GUI components, and checks for missing modules. If any missing modules are found, it calls the
        showWarning() method.

        Attributes:
        absolutePath (str): The absolute path to the main script file.
        inactiveImage (tk.PhotoImage | None): The image to be used as the window icon when modules are not installed.
        root (tk.Tk | None): The main window object.
        moduleGridder (tk.Frame | None): The frame for displaying missing module information.
        moduleYaml (bool): A flag indicating whether the required YAML module is installed.

        Returns:
        None
        """
        self.absolutePath: str = "/".join(os.path.abspath(str(sys.modules['__main__'].__file__)).split('\\')[:-1])
        self.inactiveImage: tk.PhotoImage | None = None
        self.root: tk.Tk | None = None
        self.moduleGridder: tk.Frame | None = None

        self.moduleYaml = checkYaml()
        if not self.moduleYaml:
            self.showWarning()

    def showWarning(self):
        """
        Displays a warning message and GUI components if required modules are not installed.

        Creates a new Tkinter window, sets its geometry, minimum size, and icon.
        Adds a label with a warning message and a button to continue anyway.
        Creates a frame for displaying missing module information and adds a MissingModule widget to it.
        """
        self.root = tk.Tk()
        self.root.geometry('425x175')
        self.root.wm_minsize(425, 175)
        self.root.protocol("WM_DELETE_WINDOW", exit)

        self.root.title('Warning: Some modules are not installed.')
        center_main(self.root)
        self.inactiveImage = tk.PhotoImage(file=(self.absolutePath + r'\UI\Disabled.gif'))
        self.root.wm_iconphoto(False, self.inactiveImage)

        label = tk.Label(self.root, text='Warning: Some modules are not installed.', font=self.textFont)
        label.pack()
        continueButton = tk.Button(self.root, text='Continue anyway', command=self.root.destroy)
        continueButton.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

        self.moduleGridder = tk.Frame(self.root)
        self.moduleGridder.grid_columnconfigure(0, weight=1)
        self.moduleGridder.grid_rowconfigure(0, weight=1)
        self.moduleGridder.pack(fill=tk.BOTH, expand=True, pady=(10, 5))

        missingYaml = MissingModule(self.moduleGridder, 'Yaml', 'pyyaml', self.moduleYaml)
        missingYaml.grid()

        self.root.mainloop()


def main():
    CheckModules()


main()
