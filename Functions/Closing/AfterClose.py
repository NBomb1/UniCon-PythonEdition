from Functions.Tools.DataSettings.FileDataManager import FileDataManager
from UI.MainMenu import MainMenu


def afterClose(dataManager: FileDataManager, mainMenu: MainMenu):
    dataManager.get('main').put('nickname', mainMenu.left_entry_nickname.get())
