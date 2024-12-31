from os import getcwd
from Functions.Starting.ModuleChecker import *
from Functions.Starting.MissingModule import MissingModule
import tkinter as tk

from UI.window.WindowCenter import center_main


class ModuleInstaller:
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
        self.inactiveImage: tk.PhotoImage | None = None
        self.root: tk.Tk | None = None
        self.moduleGridder: tk.Frame | None = None

        self.moduleYaml = checkYaml()
        self.pywin32 = checkPywin32()
        self.pyuac = checkPyUAC()
        if not self.moduleYaml or not self.pywin32 or not self.pyuac:
            self.showWarning()

    def showWarning(self):
        """
        Displays a warning message and GUI components if required modules are not installed.

        Creates a new Tkinter window, sets its geometry, minimum size, and icon.
        Adds a label with a warning message and a button to continue anyway.
        Creates a frame for displaying missing module information and adds a MissingModule widget to it.
        """
        self.root = tk.Tk()
        self.root.geometry('525x175')
        self.root.wm_minsize(525, 175)
        self.root.protocol("WM_DELETE_WINDOW", exit)

        self.root.title('Module installer')
        center_main(self.root)
        self.inactiveImage = tk.PhotoImage(file=(getcwd() + r'\UI\NoConnection.gif'))
        self.root.wm_iconphoto(False, self.inactiveImage)

        label = tk.Label(self.root, text='Warning: Some modules are not installed.', font=self.textFont)
        label.pack()
        continueButton = tk.Button(self.root, text='Continue anyway', command=self.root.destroy)
        continueButton.pack(side=tk.BOTTOM, fill=tk.X, pady=(10, 0))

        self.moduleGridder = tk.Frame(self.root)
        self.moduleGridder.grid_columnconfigure(0, weight=1)
        self.moduleGridder.grid_rowconfigure(0, weight=1)
        self.moduleGridder.grid_columnconfigure(1, weight=1)
        self.moduleGridder.grid_columnconfigure(2, weight=1)
        self.moduleGridder.pack(fill=tk.BOTH, expand=True, pady=(10, 5))

        missingYaml = MissingModule(self.moduleGridder, 'Yaml', 'pyyaml', self.moduleYaml)
        missingYaml.grid(column=0, row=0, sticky=tk.NSEW)

        missingYaml = MissingModule(self.moduleGridder, 'pywin32', 'pywin32', self.pywin32)
        missingYaml.grid(column=1, row=0, sticky=tk.NSEW)

        missingYaml = MissingModule(self.moduleGridder, 'pyuac', 'pyuac', self.pyuac)
        missingYaml.grid(column=2, row=0, sticky=tk.NSEW)

        self.root.mainloop()


def start():
    ModuleInstaller()
