from src.cipher import decrypt
from src.prompt import prompter
from src.record import readconf, record
from src.restful.net import login


def login_by_record():
    info = readconf()
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
        prompter.error("未知错误，登录失败！")


def login_once():
    try:
        username, password = record(save=False)
        login(username, password)
    except KeyboardInterrupt:
        exit()
    except:
        print("未知错误，登录失败！")
