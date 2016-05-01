#!/usr/bin/python
import sys

if sys.version_info[0] == 2:
    from Tkinter import *
else:
    from tkinter import *

class FullscreenWindow:

    def __init__(self):
        self.tk = Tk()
        self.tk.attributes('-zoomed', True)
        self.frame = Frame(self.tk)
        self.frame.pack()
        self.state = False
        self.tk.bind("<F11>", self.toggle_fullscreen)
        self.tk.bind("<Escape>", self.end_fullscreen)

    def toggle_fullscreen(self, event=None):
        self.state = not self.state
        self.tk.attributes('-fullscreen', self.state)
        return "break"

    def end_fullscreen(self, event=None):
        self.state = False
        self.tk.attributes('-fullscreen', self.state)
        return "break"

if __name__ == "__main__":
    w = FullscreenWindow()
    w.tk.mainloop()
