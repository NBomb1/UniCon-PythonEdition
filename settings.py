# You are not supposed to be there.
# You can make some changes in case you know what are you doing.

class MainInfo:
    startDate = '12 06 2023'


class MainMenu:
    port_from = 1024
    port_to = 49151
    switchModesDelay = 500  # ms
    max_connections_from = 1
    max_connections_to = 25
    argumentCheckAfterMainloop = 500  # ms


class SettingsMenu:
    widgetsWait = 2
    saveButtonWait = 2.05  # must be more than widgetWait


class LogManager:
    messageDelay = 0.0005  # sec


class FileDataManager:
    auto_save_interval = 30  # sec
