"""
Project started - 2023y 06m 12d

Extra Modules are used:
packaging - 23.1
"""
from UI.MainMenu import MainMenu
from Functions.logManager.logManager import Logs


def main():
    # setting up log manager
    logManager = Logs()
    logManager.registerId(0)

    MainMenu(logManager)  # Main code goes here

    logManager.closeFiles()


if __name__ == '__main__':
    main()
