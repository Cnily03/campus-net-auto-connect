import tkinter.messagebox
from config import *


def show_prompt(title, msg, type="info"):
    if type == "info":
        func = tkinter.messagebox.showinfo
    elif type == "warn":
        func = tkinter.messagebox.showwarning
    elif type == "error":
        func = tkinter.messagebox.showerror
    else:
        func = tkinter.messagebox.showinfo

    if OS == "Windows":
        print(msg)
        func(title=title, message=msg)
    else:
        print(msg)


class prompter:
    def info(msg):
        print(msg, type="info")

    def warn(msg):
        show_prompt("警告", msg, type="warn")

    def error(msg):
        show_prompt("错误", msg, type="error")
