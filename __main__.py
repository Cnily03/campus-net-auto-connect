from os import path, remove
from sys import argv
from src.restful import login_by_record, logout
from config import *


def launch_via_argv():
    exec_type = "login"
    if len(argv) > 1:
        if argv[1] in ["--login", "-l"]:
            exec_type = "login"
        if argv[1] in ["--once"]:
            exec_type = "once"
        elif argv[1] in ["--quit", "--logout", "-q"]:
            exec_type = "quit"
        elif argv[1] in ["--clear", "-c"]:
            exec_type = "clear"
        elif argv[1] in ["--reset", "-r"]:
            exec_type = "reset"
        elif argv[1] in ["--version", "-v"]:
            exec_type = "version"
        elif argv[1] in ["--help", "-h"]:
            exec_type = "help"

    if exec_type == "login":
        login_by_record()
    elif exec_type == "quit":
        logout()
    elif exec_type == "clear":
        if path.exists(CONFIG_FILE_PATH) and path.isfile(CONFIG_FILE_PATH):
            remove(CONFIG_FILE_PATH)
            print("已清除")
        else:
            print("没有要清除的身份信息")
    elif exec_type == "reset":
        if path.exists(CONFIG_FILE_PATH) and path.isfile(CONFIG_FILE_PATH):
            remove(CONFIG_FILE_PATH)
            print("已清除")
        else:
            print("没有要清除的身份信息")
        logout(is_print=False)
    elif exec_type == "version":
        print('\n'.join([
            "{}".format(__version__)
        ]))
    elif exec_type == "help":
        print('\n'.join([
            "Usage:",
            f"   {PROGRAM_NAME} [options]",
            "",
            "Options:",
            "   -l, --login" + "\t\t  登录到校园网，并缓存身份信息",
            "   --once" + "\t\t  单次登录，不缓存身份信息",
            "   -q, --quit, --logout" + "\t  登出校园网",
            "   -c, --clear" + "\t\t  清除身份缓存",
            "   -r, --reset" + "\t\t  清除身份缓存并登出校园网",
            "",
            "Copyright {} Cnily03, source code under license MIT".format(LAUNCH_TIME.date().year),
            "See souece code at https://github.com/Cnily03/compus-net-auto-connect"
        ]))


if __name__ == "__main__":
    launch_via_argv()
