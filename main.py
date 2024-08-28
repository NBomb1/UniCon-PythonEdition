"""
Project started - 2023y 06m 12d
1C Project -> Unicon

Extra libraries:
Yaml - saves&loads data from settings.
PyUAC - Checks admin rights.
win32 - Task Manager.

Started using AI tabnine to document some functions in 2024y 7m 18d.

Available app args:
* "--startAsAdmin" - starts application as admin.
* "--updated" - removes versionChanger.py if it exists, updates task in task manager and shows update message.
* "--host" - starts the server automatically.
* "--client" - starts connecting automatically. Doesn't work with "-host".
* "--noUpdateCheck" - doesn't check for updates.
* "--noAutoInstall" - disables update auto-install if enabled.
* "--doNotLoadDefaultArguments" - doesn't load default arguments that were set in program. Doesn't work in program.
* "--logsWaiterFunctionFlag" - logs contains message until at least one function is registered for that id.
* "--logsPrint" - prints logs to the console. Doesn't count as a registered function.
"""

"""
Goals:
1. Finish account module and related things.
2. Pass all authentication phases.
3. Check for Authentication scripts and move some code to Tools.
4. Permissions for clients.
5. File transfer module.
"""

from os import getcwd, chdir
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

from Functions.Starting.ArgCheck import argsCheckAfterStart, argsCheckBeforeStart, argsDefault


def main():
    # setting up log manager
    dataManager = FileDataManager()
    try:
        dataManager.create("main", getcwd() + '\\settings.yml')
        argsDefault(dataManager)
        dataManager.get('main').put('lastStart', datetime.now().timestamp())
        logManager = Logs()
        argsCheckBeforeStart(logManager)

        logManager.registerId(0)
        logManager.registerId(-1)
        logManager.registerId(-2)

        # logManager.registerFileLog(0)
        # logManager.registerFileLog(-1)

        mainMenu = MainMenu(logManager, dataManager)  # Main code goes here
        mainMenu.root.protocol("WM_DELETE_WINDOW", partial(closing, mainMenu))
        argsCheckAfterStart(mainMenu)  # checks if arguments are provided and starts server or client accordingly.
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
