"""
Project started - 2023y 06m 12d
1C Project -> Unicon

Extra libraries:
Yaml - saves&loads data from settings.

Started using AI tabnine to document some functions 2024y 7m 18d.

Available app args:
* "--updated" - removes versionChanger.py if it exists and shows update message.
* "-host" - starts the server automatically.
* "-client" - starts connecting automatically. Doesn't work with "-host".
* "-noUpdateCheck" - doesn't check for updates.
* "-noAutoInstall" - disables update auto-install if enabled.
"""
from Functions.Starting.TaskManager import afterUpdate

"""
Goals:
1. Finish account module and related things.
2. Pass all authentication phases.
3. Check for Authentication scripts and move some code to Tools.
4. Permissions for clients.
5. Chat module.
6. File transfer module.
"""

from os import getcwd, chdir, remove
from sys import argv

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
from Functions.logManager import Logs
from Functions.FileDataManager import FileDataManager
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
        argsCheck(mainMenu)  # checks if arguments are provided and starts server or client accordingly.
        mainMenu.root.mainloop()

        logManager.closeFiles()

        dataManager.get('main').put('lastClose', datetime.now().timestamp())
    except Exception:
        print(format_exc())
        ProgramStartError(format_exc())
    finally:
        dataManager.saveAll()


def argsCheck(mainMenu: MainMenu):
    try:
        if '--updated' in argv:
            try:
                remove('versionChanger.py')
            except Exception as e:
                print(f'Error while deleting versionChanger.py: {e}')
                mainMenu.logs.sendLog(f'Error while deleting versionChanger.py: {format_exc()}', 0)
            try:
                afterUpdate()
                mainMenu.logs.sendLog('Auto-startup task updated successfully.', 0)
            except Exception as e:
                mainMenu.logs.sendLog(f'Error while updating auto-startup task: {format_exc()}', 0)
            mainMenu.logs.sendLog('Program was updated successfully.', 0)
        if '-host' in argv:
            mainMenu.logs.sendLog('[Args] Starting in host mode.', 0)
            mainMenu.startServer()
        elif '-client' in argv:
            mainMenu.logs.sendLog('[Args] Starting in client mode.', 0)
            mainMenu.startClient()
        if "-noUpdateCheck" not in argv:
            if "-noAutoInstall" in argv:
                mainMenu.logs.sendLog('[Args] No update auto-install.', 0)
            mainMenu.checkForUpdates(
                mainMenu.confirmation
                if mainMenu.confirmation is not None and "-noAutoInstall" not in argv
                else False
            )
        else:
            mainMenu.logs.sendLog('[Args] No update checking.', 0)
    except Exception as e:
        mainMenu.logs.sendLog(f"Couldn't use arguments. Error: {e}", 0)


if __name__ == '__main__':
    main()
