from os import path, remove
from sys import argv
from campus_win.logger import Prompter
from campus_win.restful import login_by_record, logout, login_once
from config import *


def detect_argv(_argv, expected):
    for i in _argv:
        if i in expected:
            return True
    return False


def launch_via_argv():
    exec_type = "login"
    _argv = argv[1:]

    debug = False
    if detect_argv(_argv, ["--debug"]):
        debug = True

    if detect_argv(_argv,  ["--login", "-l"]):
        exec_type = "login"
    if detect_argv(_argv,  ["-L", "--once"]):
        exec_type = "once"
    elif detect_argv(_argv,  ["--quit", "--logout", "-q"]):
        exec_type = "quit"
    elif detect_argv(_argv,  ["--clear", "-c"]):
        exec_type = "clear"
    elif detect_argv(_argv,  ["--reset", "-r"]):
        exec_type = "reset"
    elif detect_argv(_argv,  ["--version", "-v"]):
        exec_type = "version"
    elif detect_argv(_argv, ["--help", "-h"]):
        exec_type = "help"

    if exec_type == "login":
        login_by_record(debug=debug)
    elif exec_type == "once":
        login_once(debug=debug)
    elif exec_type == "quit":
        logout(debug=debug)
    elif exec_type == "clear":
        if path.exists(CONFIG_FILE_PATH) and path.isfile(CONFIG_FILE_PATH):
            remove(CONFIG_FILE_PATH)
            Prompter.info("已清除")
        else:
            Prompter.warn("没有要清除的身份信息")
    elif exec_type == "reset":
        if path.exists(CONFIG_FILE_PATH) and path.isfile(CONFIG_FILE_PATH):
            remove(CONFIG_FILE_PATH)
            Prompter.info("已清除")
        else:
            Prompter.warn("没有要清除的身份信息")
        logout(is_log=False)
    elif exec_type == "version":
        print('\n'.join([
            "{}".format(VERSION)
        ]))
    elif exec_type == "help":
        print('\n'.join([
            "Usage:",
            f"   {PROGRAM_NAME} [options]",
            "",
            "Options:",
            "   -l, --login" + "\t\t  登录到校园网，并缓存身份信息",
            "   -L, --once" + "\t\t  单次登录，不缓存身份信息",
            "   -q, --quit, --logout" + "\t  登出校园网",
            "   -c, --clear" + "\t\t  清除身份缓存",
            "   -r, --reset" + "\t\t  清除身份缓存并登出校园网",
            "   -v, --version" + "\t  显示版本信息",
            "   -h, --help" + "\t\t  显示此帮助",
            "   --debug" + "\t\t  开启调试模式",
            "",
            "Copyright {} Cnily03, source code under license MIT".format(
                ("{}-".format(COPYRIGHT_START_YEAR) if COPYRIGHT_START_YEAR < LAUNCH_TIME.date().year else "") + str(LAUNCH_TIME.date().year)),
            "See souece code at https://github.com/Cnily03/campus-net-auto-connect"
        ]))


if __name__ == "__main__":
    launch_via_argv()
