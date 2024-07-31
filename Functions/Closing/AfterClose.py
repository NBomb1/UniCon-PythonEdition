from Functions.Tools.DataSettings.FileDataManager import FileDataManager
from UI.MainMenu import MainMenu


def afterClose(dataManager: FileDataManager, mainMenu: MainMenu):
    if mainMenu.settingsFrame.connectionSettings.checkButton_saveNickname.v.get():
        dataManager.get('main').put('nickname', mainMenu.left_entry_nickname.get())

    if mainMenu.settingsFrame.connectionSettings.checkButton_savePort.v.get():
        dataManager.get('main').put('port', mainMenu.left_spinbox_port.get())

    if mainMenu.settingsFrame.connectionSettings.checkButton_savePassword.v.get():
        dataManager.get('main').put('password', mainMenu.left_entry_password.get())

    if mainMenu.settingsFrame.connectionSettings.checkButton_saveIP.v.get():
        dataManager.get('main').put('ip', mainMenu.left_entry_ip.get())
