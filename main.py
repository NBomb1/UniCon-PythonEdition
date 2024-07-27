"""
Project started - 2023y 06m 12d
1C Project

1 Name Idea: Multifunctional network application - MNA
2 Name Idea: Modular network application - MNA
3 Name Idea: Universal Network application - UNA
4 Name Idea: Universal Connection - UniCon
ChatGPT's Idea: NetMaster

Extra libraries:
Yaml - saves&loads data from settings.

Started using AI tabnine to document some functions 2024y 7m 18d.
"""

"""
Goals:
1. Finish account module and related things.
2. Pass all authentication phases.
3. Check for Authentication scripts and move some code to Tools.
4. Auto update code.
5. Permissions for clients.
6. ModuleChecker module.
7. Chat module.
8. File transfer module.
"""

from os import getcwd, chdir, remove
from sys import argv

if '--updated' in argv:
    try:
        remove('versionChanger.py')
    except Exception as e:
        print(f'Failed to delete versionChanger.py: \n{e}')

chdir('\\'.join(__file__.split('\\')[:-1]))

from Functions.Starting import PythonVersionChecker  # checks python version

PythonVersionChecker.start()

from Functions.Starting import ModuleDownloader  # checks modules

ModuleDownloader.start()

from functools import partial

from Functions.Closing.ClosingProcess import closing

from datetime import datetime
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
        if '--updated' in argv:
            mainMenu.logs.sendLog('Program was updated successfully.', -1)
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
