import tkinter as tk
from UI.window.WindowCenter import center_main


class ProgramStartError:

    def __init__(self, exception: str):
        self.exception = exception
        self.root = tk.Tk()
        center_main(self.root)
        self.root.title("Crash")
        self.root.geometry("800x662")

        self.frameMain = tk.Frame(self.root)

        # Main
        text = f"Something went wrong due program work."
        self.label = tk.Label(self.frameMain, text=text)

        self.buttonFrame = tk.Frame(self.frameMain)
        # self.buttonLogs = tk.Button(self.buttonFrame, text='Logs')
        self.buttonClose = tk.Button(self.buttonFrame, text='Close', command=exit)

        self.frameMain.pack()
        self.label.pack()
        self.logs = tk.Label(self.frameMain, text=exception, background='gray77')
        self.logs.pack(expand=True, fill=tk.BOTH, side=tk.TOP)
        self.buttonFrame.pack()

        # self.buttonLogs.pack(side=tk.RIGHT, padx=5, ipadx=10, expand=True, anchor=tk.CENTER)
        self.buttonClose.pack(side=tk.RIGHT, padx=5, ipadx=10, expand=True, anchor=tk.E)

        self.root.mainloop()

    # The function must be done
    def save(self):
        pass
