import tkinter as tk
from tkinter.scrolledtext import ScrolledText
from UI.window.WindowCenter import center_main


class ProgramStartError:

    def __init__(self, exception: str):
        self.exception = exception
        self.root = tk.Tk()
        self.root.title("Crash")

        self.frameMain = tk.Frame(self.root)

        # Main
        text = f"An error occurred while running the program. \nError details: "
        self.label = tk.Label(self.frameMain, text=text)

        self.buttonFrame = tk.Frame(self.frameMain)
        # self.buttonLogs = tk.Button(self.buttonFrame, text='Logs')
        self.buttonClose = tk.Button(self.buttonFrame, text='Close', command=exit)

        self.frameMain.pack(expand=True, fill=tk.BOTH, pady=20, padx=50)
        self.label.pack()
        self.logs = ScrolledText(self.frameMain, background='gray77', wrap=tk.WORD)
        self.logs.insert('1.0', self.exception)
        self.logs.config(state=tk.DISABLED)  # Disable editing in ScrolledText widget
        self.logs.pack(expand=True, fill=tk.BOTH, side=tk.TOP)
        self.buttonFrame.pack()

        self.buttonClose.pack(side=tk.RIGHT, padx=5, ipadx=10, expand=True, anchor=tk.E)
        self.root.geometry("700x530")
        center_main(self.root)

        self.root.mainloop()

    # The function must be done
    def save(self):
        pass
