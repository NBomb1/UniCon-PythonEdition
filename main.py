"""
Project started - 2023y 06m 12d
1C Project

1 Name Idea: Multifunctional network application - MNA
2 Name Idea: Modular network application - MNA
3 Name Idea: Universal Network application - UNA
4 Name Idea: Universal Connection - UniCon
ChatGPT's Idea: NetMaster

Extra Modules are used:
packaging - 23.1

Extra libraries:
Yaml - saves&loads data from settings.

"""
from sys import version_info

if not (version_info.major == 3 and version_info.minor >= 10):
    input(
          "This program was started on python 3.10.\n"
          "I do not recommend use any versions above this.\n"
          "To continue press enter..."
    )

from functools import partial

from Functions.Closing.ClosingProcess import closing

"""
Goals:
1. Finish account module and related things.
2. Pass all authentication phases.
3. Check for Authentication scripts and move some code to Tools.
"""

from datetime import datetime
from os import getcwd
from traceback import format_exc

from UI.MainMenu import MainMenu
from Functions.Tools.logManager import Logs
from Functions.Tools.DataSettings.FileDataManager import FileDataManager
from UI.ProgramStartError import ProgramStartError


def main():
    # setting up log manager
    dataManager = FileDataManager()
    try:
        dataManager.create("main", getcwd() + '\\settings.yml')
        dataManager.get('main').put('lastStart', datetime.now().timestamp())

        logManager = Logs()
        logManager.registerId(0)
        logManager.registerId(-1)
        logManager.registerId(-2)
        # logManager.registerFileLog(0)
        # logManager.registerFileLog(-1)

        mainMenu = MainMenu(logManager, dataManager)  # Main code goes here
        mainMenu.root.protocol("WM_DELETE_WINDOW", partial(closing, mainMenu))
        mainMenu.root.mainloop()

        logManager.closeFiles()

        dataManager.get('main').put('lastClose', datetime.now().timestamp())
    except Exception:
        print(format_exc())
        ProgramStartError(format_exc())
    finally:
        dataManager.saveAll()


if __name__ == '__main__':
    main()
