from Crypto.Cipher import AES
import platform
import requests
from os import getenv, path, remove
from urllib import parse
import maskpass
from base64 import b64encode, b64decode
from sys import argv
import re
import json
import datetime
import hashlib
from time import sleep

__version__ = "1.0.0"
LAUNCH_TIME = datetime.datetime.now()
OS = platform.system()

FILE_NAME = ".compusnetinfo"
SAVE_DIR = {
    "Windows": "{}/".format(getenv("APPDATA")),
    "Linux": "/{}/".format(getenv("HOME")),
    "Darwin": "/var/"
}
FILE_PATH = SAVE_DIR[OS]+FILE_NAME


def sha_split_hex(string, step=16):
    hex = hashlib.sha256(string.encode("utf-8")).hexdigest()
    result = ''
    for start in range(0, step):
        for i in range(start, len(hex), step):
            result += hex[i]
    return result


AES_KEY = sha_split_hex("随便乱输一段文字", step=8).encode("utf-8")[0:16]
AES_IV = sha_split_hex("随便乱输一段文字", step=8).encode("utf-8")[0:16]
cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)


def parse_int(string: str):
    return int(''.join([x for x in string if x.isdigit()]))


def encrypt(username: str, password: str):
    return username + " | " + b64encode(cipher.encrypt(password.encode("utf-8"))).decode("utf-8")


def decrypt(ciphertext: str):
    arr = ciphertext.split(" | ")
    username = arr[0].encode("utf-8")
    password = cipher.decrypt(b64decode(arr[1].encode("utf-8"))).decode("utf-8")
    return (username, password)


def read_info():
    if not path.exists(FILE_PATH) or not path.isfile(FILE_PATH):
        return False
    lines = open(FILE_PATH, "r").readlines()
    for line in lines:
        if line.strip():
            return line.strip()
    return False


def record(save=True):
    exact_username = input("请输入账号：").strip()
    password = maskpass.askpass(prompt="请输入密码：", mask="*").strip()
    print("请选择运营商：")
    print("   1) 中国电信")
    print("   2) 中国移动")
    print("   3) 中国联通")
    operator = {
        1: "telecom",
        2: "cmcc",
        3: "unicom"
    }[parse_int(input("请输入运营商前的数字：").strip())]
    username = exact_username + "@" + operator
    if save:
        open(FILE_PATH, "w").writelines(encrypt(username, password))
    return (username, password)


def login(username: str, password: str):
    BASE_URL = f"http://10.2.5.251:801/eportal/?c=Portal&a=login&callback=dr1676944878506&login_method=1&user_account={parse.unquote(username)}&user_password={parse.unquote(password)}&wlan_user_mac=000000000000"

    HEADERS = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Host": "10.2.5.251:801",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://10.2.5.251/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50"
    }

    response = requests.get(
        url=BASE_URL,
        headers=HEADERS
    )

    res_dict: dict = json.loads(re.findall(r"^.*?\((.*)\)$", response.content.decode("utf-8"))[0])

    if "result" in res_dict.keys():
        if res_dict['result'] == "1":
            print("登录成功！")
        elif res_dict['result'] == "0":
            print("无需登录，当前已为登录状态！")
    else:
        raise Exception


def logout(is_print=True):
    BASE_URL = "http://10.2.5.251:801/eportal/?c=Portal&a=logout"

    HEADERS = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Host": "10.2.5.251:801",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://10.2.5.251/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50"
    }

    response = requests.get(
        url=BASE_URL,
        headers=HEADERS
    )

    res_dict: dict = json.loads(re.findall(r"^.*?\((.*)\)$", response.content.decode("utf-8"))[0])

    if not is_print:
        return

    if "result" in res_dict.keys():
        if res_dict['result'] == "1":
            print("已登出！")
        elif res_dict['result'] == "0":
            print("无需登出，你尚未处于登录状态！")
    else:
        raise Exception


def login_by_config():
    try:
        info = read_info()
    except:
        print("文件读取错误")
        return

    try:
        if not info == False:
            username, password = decrypt(info)
            login(username, password)
        else:
            username, password = record()
            login(username, password)
    except KeyboardInterrupt:
        exit()
    except:
        print("未知错误，登录失败！")


def login_once():
    try:
        username, password = record(save=False)
        login(username, password)
    except KeyboardInterrupt:
        exit()
    except:
        print("未知错误，登录失败！")


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
        login_by_config()
    elif exec_type == "quit":
        logout()
    elif exec_type == "clear":
        if path.exists(FILE_PATH) and path.isfile(FILE_PATH):
            remove(FILE_PATH)
    elif exec_type == "reset":
        if path.exists(FILE_PATH) and path.isfile(FILE_PATH):
            remove(FILE_PATH)
        logout(is_print=False)
    elif exec_type == "version":
        print('\n'.join([
            "{}".format(__version__)
        ]))
    elif exec_type == "help":
        print('\n'.join([
            "This is the command help of Compus Net Auto Connection program:",
            "   -l, --login" + "\t\t  登录到校园网，并缓存身份信息",
            "   --once" + "\t\t  单次登录，不缓存身份信息",
            "   -q, --quit, --logout" + "\t  登出校园网",
            "   -c, --clear" + "\t\t  清除身份缓存",
            "   -r, --reset" + "\t\t  清除身份缓存并登出校园网",
            "Copyright {} Cnily03, source code under license MIT".format(LAUNCH_TIME.date().year)
        ]))


if __name__ == "__main__":
    launch_via_argv()
    print("The window will be closed in 2 second...")
    sleep(2)
