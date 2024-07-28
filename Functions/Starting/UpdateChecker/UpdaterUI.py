import tkinter as tk
from datetime import datetime
from functools import partial
from os import chdir, getpid
from os import path as pathOs
from sys import path
from threading import Thread, Timer
from time import sleep

import fileDownloader

# thisPath = pathOs.dirname(pathOs.abspath(__file__))
# projectPath = pathOs.join(thisPath, '..', '..', '..')
thisPath = pathOs.dirname(pathOs.abspath(__file__))
projectPath = '\\'.join(thisPath.split('\\')[:-3])
downloadPath = projectPath + '\\new_version'

path.append(projectPath)
chdir(thisPath)

import UpdaterInfo as info
from Functions.Starting.UpdateChecker.checkVersion import check_for_updates
from UI.TKinter_addons.Text_chat import ChatText
from UI.window.WindowCenter import center_main
from UI.Info import Info
from Functions.Starting.UpdateChecker import Processes

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
        self.root.after(4000, self.checkVersion)
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

        def check_version_thread():
            res = check_for_updates(
                info.URL,
                info.GITHUB_TOKEN,
                Info.version,  # other file
                info.CLASS_NAME,
                info.ATTRIBUTE_NAME
            )
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
            Timer(6, function=self.download_update).start()

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
        self.createMessage('Downloading update...')
        self.root.update()
        fileDownloader.update_program(self.createMessage, downloadPath)
        self.isFinished = True
        # TODO: Download and install the update
        self.createMessage('Update downloaded successfully!')
        self.restart_program()

    def restart_program(self):
        # source_file = thisPath + '\\versionChanger.py'

        self.root.after(1000, lambda: self.createMessage('Restarting in 5 seconds...'))
        self.root.after(2000, lambda: self.createMessage('Restarting in 4 seconds...'))
        self.root.after(3000, lambda: self.createMessage('Restarting in 3 seconds...'))
        self.root.after(4000, lambda: self.createMessage('Restarting in 2 seconds...'))
        self.root.after(5000, lambda: self.createMessage('Restarting in 1 seconds...'))
        self.root.after(6000, lambda: self.createMessage('Restarting in 0 seconds...'))
        self.root.after(7500, lambda: Processes.run_independent_process(
            thisPath + '\\versionChanger.py',
            projectPath + '\\new_version',
            projectPath,
            f"{getpid()}"  # Идентификатор текущего процесса
        )
                        )


if __name__ == '__main__':
    UpdaterUI()
