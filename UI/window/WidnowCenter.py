import tkinter as tk


def center_main(win: tk.Tk):
    # code was copied and pasted from internet
    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()


def center_child(child: tk.Toplevel, root: tk.Tk):
    x = root.winfo_x() + root.winfo_width() / 2 - (400 / 2)
    y = root.winfo_y() + root.winfo_height() / 2 - (300 / 2)
    child.geometry('%dx%d+%d+%d' % (child.winfo_width(), child.winfo_height(), x, y))
