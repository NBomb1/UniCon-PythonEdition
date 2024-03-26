"""
Project started - 2023y 06m 12d

1 Name Idea: Multifunctional network application - MNA
2 Name Idea: Modular network application - MNA
3 Name Idea: Universal Network application - UNA
4 Name Idea: Universal Connection - UniCon
ChatGPT's Idea: NetMaster

Extra Modules are used:
packaging - 23.1

Extra libraries:
No

"""

"""
Goals:
1. Finish account module and related things.
2. Pass all authentication phases.
3. Function execution before program closes.
"""

from datetime import datetime
from os import getcwd
from traceback import format_exc

from Functions.Tools.MultipleStartRestriction import MultipleStartRestriction
from UI.MainMenu import MainMenu
from Functions.Tools.logManager import Logs
from Functions.Tools.DataSettings.FileDataManager import DataManager
from UI.ProgramStartError import ProgramStartError


def main():
    # setting up log manager
    try:
        # startCheck = MultipleStartRestriction()
        # if not startCheck.checkIsLocked():
        #     raise Exception("Program has already been started!")
        # startCheck.lock_file()

        dataManager = DataManager()
        dataManager.create("main", getcwd() + '\\settings.yml')
        dataManager.get('main').put('lastStart', datetime.now().timestamp())

        logManager = Logs()
        logManager.registerId(0)
        logManager.registerId(-1)
        # logManager.registerFileLog(0)
        # logManager.registerFileLog(-1)

        MainMenu(logManager, dataManager)  # Main code goes here

        logManager.closeFiles()

        dataManager.get('main').put('lastClose', datetime.now().timestamp())
        dataManager.saveAll()
    except Exception:
        ProgramStartError(format_exc())


if __name__ == '__main__':
    main()
