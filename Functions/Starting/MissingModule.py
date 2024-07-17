import sys
import tkinter as tk
from threading import Thread


class MissingModule(tk.Frame):
    """
    A class to represent a missing module in a Python application.
    It provides a GUI interface to install the module using pip.

    Attributes:
    - moduleName: The name of the module.
    - pipName: The name of the module in pip.
    - root: The root widget of the application.
    - moduleLabel: A Label widget to display the module name.
    - moduleButtonInstall: A Button widget to install the module.
    - resultLabel: A Label widget to display the installation result.

    Methods:
    - __init__(self, root: tk.Widget, moduleName: str, pipName: str, isInstalled: bool):
        Initializes the MissingModule instance.
    - installModule(self):
        Installs the module using pip in a separate thread.
    """

    def __init__(self, root: tk.Widget, moduleName: str, pipName: str, isInstalled: bool):
        super().__init__(root)
        self.moduleName = moduleName
        self.pipName = pipName
        self.root = root

        self.moduleLabel = tk.Label(self, text=f"{moduleName}")
        self.moduleButtonInstall = tk.Button(self, text="Install module", command=self.installModule)
        self.moduleButtonInstall.configure(state=tk.DISABLED if isInstalled else tk.NORMAL)
        self.resultLabel = tk.Label(self, text='Press button to install')

        self.moduleLabel.pack()
        self.moduleButtonInstall.pack()
        self.resultLabel.pack()

    def installModule(self):
        """
        Installs the module using pip in a separate thread.
        """
        self.moduleButtonInstall.configure(state=tk.DISABLED)
        self.resultLabel.configure(text="Installing module...")

        def install_thread():
            try:
                from subprocess import check_call
                check_call([sys.executable, '-m', 'pip', 'install', self.pipName], timeout=10)
                self.resultLabel.configure(text='Module installed successfully.')
            except Exception as e:
                print(f"Error installing module '{self.moduleName}': {e}")
                self.resultLabel.config(text=f"Couldn't install module.\n"
                                             f"Try installing it manually.\n")
                self.moduleButtonInstall.configure(state=tk.NORMAL)
            self.resultLabel.pack()

        Thread(target=install_thread, daemon=True).start()
