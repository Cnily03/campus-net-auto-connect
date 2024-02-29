import re
import json
import requests
from campus_win.logger import Logger, Prompter
from urllib import parse
from campus_win.restful.net import *


def login(username: str, password: str):
    BASE_URL = f"http://10.2.5.251:801/eportal/?c=Portal&a=login&login_method=1&user_account={parse.unquote(username)}&user_password={parse.unquote(password)}&wlan_user_mac=000000000000"

    HEADERS = {
        "Accept": "*/*",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Host": "10.2.5.251:801",
        "Proxy-Connection": "keep-alive",
        "Referer": "http://10.2.5.251/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50"
    }

    TIMEOUT = 5

    Logger.log("正在连接到校园网...")
    try:
        response = requests.get(
            url=BASE_URL,
            headers=HEADERS,
            timeout=TIMEOUT
        )
    except requests.exceptions.Timeout:
        Prompter.error("连接超时，请检查是否连接校园网。")
        return
    except:
        raise

    res_dict: dict = json.loads(re.findall(r"^.*?\((.*)\)$", response.content.decode("utf-8"))[0])

    if "result" in res_dict.keys():
        if res_dict['result'] == "1":
            Prompter.info("登录成功！")
            return True
        elif res_dict['result'] == "0":
            if "ret_code" in res_dict.keys():
                if res_dict["ret_code"] == "1":
                    Prompter.warn("统一身份认证用户名密码错误！")
                if res_dict["ret_code"] == "2":
                    Prompter.warn("无需登录，当前已为登录状态！")
    else:
        raise Exception


def logout(is_log=True, debug=False):
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

    TIMEOUT = 5

    if is_log:
        Logger.log("正在连接到校园网...")
    try:
        response = requests.get(
            url=BASE_URL,
            headers=HEADERS,
            timeout=TIMEOUT
        )
    except requests.exceptions.Timeout:
        Prompter.error("连接超时，请检查是否连接校园网。")
        return
    except:
        if debug:
            raise
        Prompter.error("未知错误！")

    res_dict: dict = json.loads(re.findall(r"^.*?\((.*)\)$", response.content.decode("utf-8"))[0])

    if not is_log:
        return

    if "result" in res_dict.keys():
        if res_dict['result'] == "1":
            Prompter.info("注销成功！")
        elif res_dict['result'] == "0":
            Prompter.warn("无需注销，你尚未处于登录状态！")
    else:
        raise Exception
