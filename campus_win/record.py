import sys
import maskpass

from .logger import Prompter
from config import *
from os import path
from .cipher import encrypt


def parse_int(string: str):
    return int('0'+''.join([x for x in string if x.isdigit()]))


def readconf():
    if not path.exists(CONFIG_FILE_PATH) or not path.isfile(CONFIG_FILE_PATH):
        return False

    try:
        lines = open(CONFIG_FILE_PATH, "r").readlines()
    except KeyboardInterrupt:
        sys.exit()
    except:
        Prompter.error("文件读取错误")

    for line in lines:
        if line.strip():
            return line.strip()
    return False


def saveconf(username, password):
    open(CONFIG_FILE_PATH, "w").writelines(encrypt(username, password))


def select_operator():
    operators = {
        1: "telecom",
        2: "cmcc",
        3: "unicom"
    }
    print("请选择运营商：")
    print("   1) 中国电信")
    print("   2) 中国移动")
    print("   3) 中国联通")
    op_num = 0
    while op_num < 1 or op_num > len(operators.keys()):
        op_num = parse_int(input("请输入运营商前的数字："))
    return operators[op_num]


def record(save=True):
    exact_username = ''
    password = ''
    while not exact_username:
        exact_username = input("请输入账号：").strip()
    while not password:
        password = maskpass.askpass(prompt="请输入密码：", mask="*").strip()
    operator = select_operator()

    username = exact_username + "@" + operator
    if save:
        saveconf(username, password)
    return (username, password)
