import shutil
import tkinter as tk
import traceback
from datetime import datetime
from functools import partial
from os import chdir, getcwd
from os import path as pathOs
from subprocess import PIPE, Popen
from sys import path, executable
from threading import Thread, Timer
from time import sleep
from traceback import format_exc

import fileDownloader

# thisPath = pathOs.dirname(pathOs.abspath(__file__))
# projectPath = pathOs.join(thisPath, '..', '..', '..')
thisPath = pathOs.dirname(pathOs.abspath(__file__))
projectPath = '\\'.join(thisPath.split('\\')[:-3])
downloadPath = projectPath + '\\new_version'

path.append(projectPath)
chdir(projectPath)

import UpdaterInfo as info
from Functions.Starting.UpdateChecker.checkVersion import check_for_updates
from UI.TKinter_addons.Text_chat import ChatText
from UI.window.WindowCenter import center_main
from UI.Info import Info

sleep(1)


class UpdaterUI:
    uniconUpdateText = [".", "..", "..."]
    isFinished = False
    messageQueue = []

    # uniconUpdateText = ["--", '\\', '|', '/']

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('UniCon updater')

        self.photoDisabled = tk.PhotoImage(file=thisPath + r'\UpdaterIcon.gif')
        self.root.wm_iconphoto(False, self.photoDisabled)

        self.labelUpdateRunning = tk.Label(self.root, justify=tk.LEFT, width=1000)
        self.logs = ChatText(self.root)

        self.labelUpdateRunning.pack(fill=tk.X, anchor=tk.N, side=tk.TOP)
        self.logs.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))

        self.root.geometry('850x500')
        center_main(self.root)

        self.animationUpdateRunning(0)
        self.root.wm_minsize(400, 170)
        Thread(target=self.logsHandler, daemon=True).start()
        self.createMessage('UniCon updater is running...')
        self.root.after(2000, self.checkVersion)
        self.root.mainloop()

    def animationUpdateRunning(self, animation=0):
        if self.isFinished:
            self.labelUpdateRunning.configure(text='Update finished!')
            return
        base_text = 'UniCon updater is running'
        max_length = len(base_text + max(self.uniconUpdateText, key=len))
        current_text = base_text + self.uniconUpdateText[animation]
        padded_text = current_text.ljust(max_length)
        self.labelUpdateRunning.configure(text=padded_text)
        self.root.after(
            700, lambda: self.animationUpdateRunning(
                animation=(animation + 1) % len(self.uniconUpdateText))
        )

    def checkVersion(self):
        self.createMessage(f'Current version {Info.version}')
        self.createMessage('Checking for updates...')
        defaultRetries = 5
        retries = defaultRetries

        def check_version_thread():
            nonlocal retries
            try:
                res = check_for_updates(
                    info.URL,
                    info.GITHUB_TOKEN,
                    Info.version,  # other file
                    info.CLASS_NAME,
                    info.ATTRIBUTE_NAME,
                    info.REPO_OWNER,
                    info.REPO_NAME,
                    info.BRANCH,
                    info.GITHUB_API_URL,
                    False
                )
            except Exception as e:
                if retries <= 0:
                    self.createMessage('Max retries reached. Check your internet connection.')
                    self.errorWhileUpdatingProgram()
                    self.isFinished = True
                    return
                retries -= 1
                self.createMessage('An error occurred while checking updates.')
                self.createMessage(f'Exception full: {traceback.format_exc()}.\n')
                self.createMessage(f'Exception: {e}.')
                self.createMessage(f'{retries} out of {defaultRetries} left. Next retry starts in 3 seconds.')
                sleep(3)
                self.createMessage('Retrying...')
                check_version_thread()
            if res is None:
                self.createMessage("Couldn't check for updates. Please check your internet connection.")
                return
            self.createMessage(f'New version: {res.newVersion}')
            if not res.isOutdated:
                self.createMessage('You are using the latest version.')
                self.isFinished = True
                return

            self.createMessage('A new update is available!')
            self.createMessage(f'Starting update...')
            Timer(1, function=self.download_update).start()

        Thread(target=check_version_thread, daemon=True).start()

    def createMessage(self, message):
        self.messageQueue.append(partial(self.logs.create_message,
                                         {
                                             'message': message
                                         },
                                         datetime.now(),
                                         '<{time}> {message}',
                                         {
                                             'message': 'system-message'
                                         }
                                         ))

    def logsHandler(self):
        while True:
            for message in self.messageQueue:
                message()
                self.messageQueue.remove(message)
            sleep(0.001)

    def download_update(self):
        try:
            self.createMessage('Downloading update...')
            self.root.update()
            fileDownloader.update_program(self.createMessage, downloadPath)
            self.isFinished = True
            self.createMessage('Update downloaded successfully!')
            self.restart_program()
        except Exception as e:
            self.errorWhileUpdatingProgram()

    def restart_program(self):
        try:
            source_file = pathOs.join(thisPath + '\\versionChanger.py')
            to_file = (projectPath + '\\versionChanger.py')
            self.createMessage('source_file: %s' % source_file)
            self.createMessage('to_file: %s' % to_file)
            # to_file = pathOs.join(projectPath, 'versionChanger.py')
            shutil.copyfile(source_file, to_file)

            self.root.after(1000, lambda: self.createMessage('Restarting in 5 seconds...'))
            self.root.after(2000, lambda: self.createMessage('Restarting in 4 seconds...'))
            self.root.after(3000, lambda: self.createMessage('Restarting in 3 seconds...'))
            self.root.after(4000, lambda: self.createMessage('Restarting in 2 seconds...'))
            self.root.after(5000, lambda: self.createMessage('Restarting in 1 seconds...'))
            self.root.after(6000, lambda: self.createMessage('Restarting in 0 seconds...'))
            # self.root.after(7500, lambda: Processes.run_independent_process(
            #     to_file,
            #     # thisPath + '\\versionChanger.py',
            #     pathOs.join(projectPath, 'new_version'),
            #     projectPath,
            #     f"{getpid()}",  # Идентификатор текущего процесса
            #     close=False
            # )
            #                 )
            self.root.after(7500, lambda:
            Popen(
                [executable, to_file, pathOs.join(projectPath, 'new_version'), projectPath],
                creationflags=0x00000008,
                stdout=PIPE,
                stderr=PIPE,
                close_fds=False,
                cwd=getcwd()
            )
                            )
            self.root.after(8000, self.root.destroy)
            # self.root.after(12500, self.root.destroy)
        except Exception as e:
            self.createMessage(f'Error restarting program: {str(e)}')
            self.createMessage(f'Showing format exception: {format_exc()}')

    def errorWhileUpdatingProgram(self):
        self.root.bell()
        self.createMessage(f'Exception full: {traceback.format_exc()}.\n')
        sleep(0.01)
        self.createMessage('An error occurred while updating.')
        self.createMessage('Program will restart in 10 seconds. This window will not close.')
        to_file = (projectPath + '\\main.py')
        self.root.after(10000, lambda:
        Popen(
            (executable, to_file, "--noUpdateCheck"),
            creationflags=0x00000008,
            stdout=PIPE,
            stderr=PIPE,
            close_fds=False,
            cwd=getcwd()
        )
                        )

if __name__ == '__main__':
    UpdaterUI()
