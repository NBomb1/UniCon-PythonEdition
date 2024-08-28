from Functions.FileDataManager import FileDataManager
from UI.MainMenu import MainMenu


def beforeClose(dataManager: FileDataManager, mainMenu: MainMenu):
    if mainMenu.settingsFrame.connectionSettings.checkButton_saveNickname.savedData:
        dataManager.get('main').put('nickname', mainMenu.left_entry_nickname.get())

    if mainMenu.settingsFrame.connectionSettings.checkButton_savePort.savedData:
        dataManager.get('main').put('port', mainMenu.left_spinbox_port.get())

    if mainMenu.settingsFrame.connectionSettings.checkButton_savePassword.savedData:
        dataManager.get('main').put('password', mainMenu.left_entry_password.get())

    if mainMenu.settingsFrame.connectionSettings.checkButton_saveIP.savedData:
        dataManager.get('main').put('ip', mainMenu.left_entry_ip.get())

    if mainMenu.settingsFrame.connectionSettings.checkButton_saveMaxConns.savedData:
        dataManager.get('main').put('maxConnections', mainMenu.maxConnections.get())
