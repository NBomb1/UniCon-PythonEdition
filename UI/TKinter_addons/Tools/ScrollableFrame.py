import tkinter as tk


class ScrollableFrame(tk.Frame):
    def __init__(self, master, *args, **kwargs):
        tk.Frame.__init__(self, master, *args, **kwargs)

        self.canvas = tk.Canvas(self, highlightthickness=0)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)

        self.inner_frame = tk.Frame(self.canvas)

        self.canvas_frame_id = self.canvas.create_window((0, 0), window=self.inner_frame, anchor="nw")
        self.inner_frame_id = self.inner_frame.winfo_id()

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.bind("<Configure>", self._on_canvas_configure)
        self.inner_frame.bind("<Configure>", self._on_inner_frame_configure)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_canvas_configure(self, event):
        self.canvas.itemconfig(self.canvas_frame_id, width=event.width)  # Используем self.canvas_frame_id

    def _on_inner_frame_configure(self, event):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_mousewheel(self, event):
        if self.canvas.bbox("all")[3] > self.canvas.winfo_height():
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_enter(self, event):
        self.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_leave(self, event):
        self.unbind_all("<MouseWheel>")
