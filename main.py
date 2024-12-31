"""
UniCon - 2023y 06m 12d.

Extra libraries:
Yaml - saves&loads data from settings.
PyUAC - Checks admin rights.
win32 - Task Manager.

Available app args:
* "--startAsAdmin" - starts application as admin.
* "--updated" - removes versionChanger.py if it exists, updates task in task manager and shows update message.
* "--host", "-h" - starts the server automatically.
* "--client", "-c" - starts connecting automatically. Doesn't work with "-host".
* "--autoReconnection" - Creates a loop that tries to connect to the server after a period of time (20 sec by default).
* "--noUpdateCheck" - doesn't check for updates.
* "--noAutoInstall" - disables update auto-install if enabled.
* "--doNotLoadDefaultArguments" - doesn't load default arguments that were set in program. Doesn't work in default args.
* "--logsWaiterFunctionFlag" - logs contains message until at least one function is registered for that id.
* "--logsPrint" - prints logs to the console. Doesn't count as a registered function.
* "--exportLogs" - exports program logs to Logs folder.

"""

from UI.Info import Info
"""
Goals:
1. Finish account module and related things.
2. Pass all authentication phases.
3. Check for Authentication scripts and move some code to Tools.
4. Permissions for clients.
5. File transfer module.
6. Reconnection system.
7. Using the custom tkinter module.
8. Add program tabs for help and API description and so on.
9. Rework the messageTransfer system.
10. Enhance PingManager.
11. Register MessageTransfer through API.
12. Add timeout to connection phase.
"""

"""
Update plan (Might change at any moment):
0.1.x - Adding main features.
0.2.x - UI update; TSL 1.3 as experimental feature, using Semantic Versioning & upgrading system improving.

1. - API rework.
2. - Network system rework; TSL 1.3 turned on by default.
3. - Adding more features and flexible settings.
4. - Multilanguage support(EN, RU).
5. - Code cleanup & enhancement.

1.0.0 - Release, full implementation of TSL 1.3, all versions(modules and ect) will be changed to 1.0.0.
2.0.0 - Merging to Kivy or -->pyqt5.
"""

"""
0.2.0 IDEAS
1. Moving to CustomTkinter
2. Right click options.
3. (Textchat widget) right click options (copy, select-all, show date)
4. Server options will be moved to new widget.
5. Left side will be used for modules and build in features.
6. Hide widget by right clicking (experimental/not necessary).
7. Module viewing as built-in feature.
8. Adjusting font size.
9. Showing extra libraries in "About".
10. Enhance widgets.
11. Reserve modules ids and make conflict message.
12. Module Logs sendLog update.
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

import settings
from UI.MainMenu import MainMenu
from Functions.logManager import Logs
from Functions.FileDataManager import FileDataManager
from UI.ProgramStartError import ProgramStartError

from Functions.Starting.ArgCheck import \
    argsCheckAfterStart, argsCheckBeforeStart, argsDefault, checkArguments, argsCheckAfterMainloop


def main():
    dataManager = FileDataManager()
    try:
        dataManager.create("main", getcwd() + '\\settings.yml')
        checkArguments()
        argsDefault(dataManager)
        dataManager.get('main').put('lastStart', datetime.now().timestamp())
        logManager = Logs()  # Creating log manager
        argsCheckBeforeStart(logManager)

        logManager.registerId(0)
        logManager.registerId(-1)
        logManager.registerId(-2)
        logManager.registerId(-3)
        logManager.registerId("All ids")

        mainMenu = MainMenu(logManager, dataManager)  # Main code goes here
        logManager.sendLog(f"[UniCon] Version: {Info.version}.", 0)
        mainMenu.root.protocol("WM_DELETE_WINDOW", partial(closing, mainMenu))
        mainMenu.root.protocol("WM_SAVE_YOURSELF", partial(closing, mainMenu, False))
        argsCheckAfterStart(mainMenu)  # checks if arguments are provided and starts server or client accordingly.
        mainMenu.root.after(settings.MainMenu.argumentCheckAfterMainloop, lambda: argsCheckAfterMainloop(mainMenu))
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
