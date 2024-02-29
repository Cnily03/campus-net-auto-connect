import tkinter.messagebox
from config import *
import psutil


def is_console():
    image_name = 'explorer.exe'
    s = psutil.Process().parent()
    if s.name() == image_name or s.parent().name() == image_name:
        return False
    return True


IS_CONSOLE = is_console()


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
        Logger.auto(msg, type)
        func(title=title, message=msg)
    else:
        Logger.auto(msg, type)


class logger:
    def auto(msg, type="log"):
        if type == "log":
            Logger.log(msg)
        elif type == "info":
            Logger.info(msg)
        elif type == "warn":
            Logger.warn(msg)
        elif type == "error":
            Logger.error(msg)
        else:
            Logger.log(msg)

    def log(msg):
        print(msg)

    def info(msg):
        print("[INFO] {}".format(msg))

    def warn(msg):
        print("[WARN] {}".format(msg))

    def error(msg):
        print("[ERROR] {}".format(msg))


class prompter:
    def info(msg):
        show_prompt("提示", msg, type="info")

    def warn(msg):
        show_prompt("警告", msg, type="warn")

    def error(msg):
        show_prompt("错误", msg, type="error")


Logger = logger

Prompter = Logger if IS_CONSOLE else prompter
