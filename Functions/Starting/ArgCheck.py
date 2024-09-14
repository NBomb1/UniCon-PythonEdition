import sys
import traceback
from os import remove, getcwd, path
from sys import argv
from traceback import format_exc
import shlex
import argparse
from tkinter import messagebox

from Functions.FileDataManager import FileDataManager
from Functions.Starting import TaskManager
from Functions.logManager import Logs
from UI.MainMenu import MainMenu

args = argparse.Namespace()
setattr(args, "_unknown_args", None)
setattr(args, "_error", None)


def argsCheckAfterStart(mainMenu: MainMenu):
    try:
        if args.updated:
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
        if args.host:
            mainMenu.logs.sendLog('[Args] Starting in host mode.', 0)
            mainMenu.startServer()
        elif args.client:
            mainMenu.logs.sendLog('[Args] Starting in client mode.', 0)
            mainMenu.startClient()
        if not args.noUpdateCheck:
            if args.noAutoInstall:
                mainMenu.logs.sendLog('[Args] No update auto-install.', 0)
            mainMenu.checkForUpdates(
                mainMenu.confirmation
                if mainMenu.confirmation is not None and not args.noAutoInstall
                else False
            )
        else:
            mainMenu.logs.sendLog('[Args] No update checking.', 0)
        if args.autoReconnection is not None:
            mainMenu.root.after(
                                args.autoReconnection * 1000,
                                lambda: mainMenu.autoReconnection(args.autoReconnection)
                                )
    except Exception as e:
        mainMenu.logs.sendLog(f"[Args] Loading arguments error: {traceback.format_exc()}", 0)
        args._error = e if args._error is None else args._error + f'\n{e}'


def argsCheckAfterMainloop(mainMenu: MainMenu):
    if args._unknown_args:
        mainMenu.logs.sendLog(f'[Args] Found unknown arguments: {args._unknown_args}', 0)
        messagebox.showinfo('Warning', f'Unknown arguments found:\n{args._unknown_args}')
    if args._error is not None:
        messagebox.showerror('ERROR', f"An error occurred while getting program arguments.\n{args._error}")


def argsCheckBeforeStart(logs: Logs):
    try:
        if args.startAsAdmin:
            startAsAdmin()
        if args.logsWaiterFunctionFlag:
            logs.enableFunctionWaiter()
        if args.logsPrint:
            logs.showLogs()
        print(args.exportLogs)
        for i in args.exportLogs:
            logs.registerFileLog(int(i), True)
    except Exception as e:
        print(format_exc())


def startAsAdmin():
    if TaskManager.disable or TaskManager.isAdmin:
        return

    args = [path.join(getcwd(), 'main.py')]
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


def argsDefault(data: FileDataManager):
    main = data.get('main')
    if main.get('checkButton_IKnowWhatIAmDoing') is not None and main.get('checkButton_IKnowWhatIAmDoing'):
        if args.doNotLoadDefaultArguments:
            return
        res = main.get('entry_defaultArguments').__str__()
        res = shlex.split(res)
        argv.extend(res)
        checkArguments(True)
        print('New arguments:', res)
        print('Now arguments:', argv)


def checkArguments(disableHelp=False):
    parse = argparse.ArgumentParser(
        prog='UniCon',
        description='UniCon project 2023-06-12.',
        exit_on_error=False,
        conflict_handler='resolve',
        add_help=False
    )
    if not disableHelp:
        parse.add_argument(
            '--help',
            '-help',
            action='help', default=argparse.SUPPRESS,
            help='show this help message and exit'
        )
    parse.add_argument(
        "--startAsAdmin",
        help="Starts application as admin",
        action='store_true'
    )
    parse.add_argument(
        '--updated',
        help="Removes versionChanger.py if it exists, updates task in task manager and shows update message.",
        action='store_true'
    )
    parse.add_argument(
        '-h',
        '--host',
        help='Starts the server automatically.',
        action='store_true'
    )
    parse.add_argument(
        '-c',
        '--client',
        help="""Starts connecting automatically. Doesn't work with "-host".""",
        action='store_true'
    )
    # finish the idea later
    parse.add_argument(
        '--autoReconnection',
        help="Creates a loop that tries to connect to the server after a period of time (20 sec by default). "
             "Disables beep sound when connection fails.",
        nargs='?',
        type=int,
        const=20
    )
    parse.add_argument(
        '--noUpdateCheck',
        help="Doesn't check for updates.",
        action='store_true'
    )
    parse.add_argument(
        '--noAutoInstall',
        help='Disables update auto-install if enabled.',
        action='store_true'
    )
    parse.add_argument(
        '--doNotLoadDefaultArguments',
        help="Doesn't load default arguments that were set in program. Doesn't work in program.",
        action='store_true'
    )
    parse.add_argument(
        '--logsWaiterFunctionFlag',
        help="Logs contains message until at least one function is registered for that id.",
        action='store_true'
    )
    parse.add_argument(
        '--logsPrint',
        help="Prints logs to the console. Doesn't count as a registered function.",
        action='store_true'
    )
    parse.add_argument(
        '--exportLogs',
        default=(),
        help="Exports logs to files.",
        action='store',
        nargs='+',
    )
    try:
        unknown_args = parse.parse_known_args(namespace=args)[1]
        args._unknown_args = unknown_args
        args.error = None
    except Exception as e:
        args.error = format_exc()
    # print(args.exportLogs)
