"""
Project started - 2023y 06m 12d

1 Name Idea: Multifunctional network application - MNA
2 Name Idea: Modular network application - MNA
ChatGPT's Idea: NetMaster

Extra Modules are used:
packaging - 23.1
"""
from UI.MainMenu import MainMenu
from Functions.Tools.logManager import Logs


def main():
    # setting up log manager
    logManager = Logs()
    logManager.registerId(0)
    logManager.registerId(-1)
    # logManager.registerFileLog(0)
    # logManager.registerFileLog(-1)

    MainMenu(logManager)  # Main code goes here

    logManager.closeFiles()


if __name__ == '__main__':
    main()
