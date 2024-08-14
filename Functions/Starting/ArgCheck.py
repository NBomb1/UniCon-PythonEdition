import sys
from os import remove, getcwd, path
from sys import argv
from traceback import format_exc
import shlex

from Functions.FileDataManager import FileDataManager
from Functions.Starting import TaskManager
from UI.MainMenu import MainMenu


def argsCheckAfterStart(mainMenu: MainMenu):
    try:
        if '--updated' in argv:
            try:
                remove('versionChanger.py')
            except Exception as e:
                print(f'Error while deleting versionChanger.py: {e}')
                mainMenu.logs.sendLog(f'Error while deleting versionChanger.py: {format_exc()}', 0)
            try:
                TaskManager.afterUpdate()
                mainMenu.logs.sendLog('Auto-startup task updated successfully.', 0)
            except Exception as e:
                mainMenu.logs.sendLog(f'Error while updating auto-startup task: {format_exc()}', 0)
            mainMenu.logs.sendLog('Program was updated successfully.', 0)
        if '--host' in argv:
            mainMenu.logs.sendLog('[Args] Starting in host mode.', 0)
            mainMenu.startServer()
        elif '--client' in argv:
            mainMenu.logs.sendLog('[Args] Starting in client mode.', 0)
            mainMenu.startClient()
        if "--noUpdateCheck" not in argv:
            if "--noAutoInstall" in argv:
                mainMenu.logs.sendLog('[Args] No update auto-install.', 0)
            mainMenu.checkForUpdates(
                mainMenu.confirmation
                if mainMenu.confirmation is not None and "--noAutoInstall" not in argv
                else False
            )
        else:
            mainMenu.logs.sendLog('[Args] No update checking.', 0)
    except Exception as e:
        mainMenu.logs.sendLog(f"Couldn't use arguments. Error: {e}", 0)


def argsCheckBeforeStart():
    try:
        if '--startAsAdmin' in argv:

            if TaskManager.disable or TaskManager.isAdmin:
                return

            args = [path.join(getcwd(), 'main.py'), '--startAsAdmin']

            if not sys.platform.startswith('win'):
                raise EnvironmentError("This script only works on Windows.")
            for i in range(0, len(args)):
                args[i] = '"' + args[i] + '"'

            import win32com.shell.shell as shell
            import win32con
            shell.ShellExecuteEx(
                lpVerb='runas',
                # lpFile='"'+sys.executable + '"',
                lpFile='"' + sys.executable + '"',
                nShow=win32con.SW_NORMAL,
                lpParameters=' '.join(args)
            )
            exit()
    except Exception as e:
        print(format_exc())


def argsDefault(data: FileDataManager):
    main = data.get('main')
    if main.get('checkButton_IKnowWhatIAmDoing') is not None and main.get('checkButton_IKnowWhatIAmDoing'):
        if "--doNotLoadDefaultArguments" in argv:
            return
        res = main.get('entry_defaultArguments').__str__()
        res = shlex.split(res)
        argv.extend(res)
        print('New arguments:', res)
        print('Now arguments:', argv)
