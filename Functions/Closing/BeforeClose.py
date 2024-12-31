from Functions.FileDataManager import FileDataManager
from UI.MainMenu import MainMenu


def beforeClose(dataManager: FileDataManager, mainMenu: MainMenu, askBeforeClosing: bool):
    saveData(dataManager, mainMenu)
    sendCloseInfo(mainMenu, 'Program was closed' if askBeforeClosing else 'PC is shutting down')


def saveData(dataManager: FileDataManager, mainMenu: MainMenu):
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


def sendCloseInfo(mainMenu: MainMenu, reason):
    accountManager = mainMenu.accountManager
    if accountManager.getIsServer() is not None:
        if accountManager.getSelfAccount().socket is None:
            return  # client could be still in connection phase, which means that we don't have to do anything

        if not accountManager.getIsServer():
            accountManager.getSelfAccount().socket.send_message(
                'close',
                False,
                reason=reason
            )
        else:
            self = accountManager.getSelfAccount()
            for i in accountManager.getParticipants().copy():
                accountManager.kickAccount(self, i, reason, True)
        mainMenu.closeConnection()
