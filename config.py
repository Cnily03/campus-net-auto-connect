import datetime
from os import getenv
import platform

# ================================

PROGRAM_NAME = "AutoConnect"
VERSION = "1.0.1"
CONFIG_FILE_NAME = ".campusnetinfo"

AES_KEY_TEXT = "随便乱输一段文字"
AES_IV_TEXT = "随便乱输一段文字"

CONFIG_SAVE_DIR = {
    "Windows": "{}/".format(getenv("APPDATA")),
    "Linux": "/{}/".format(getenv("HOME")),
    "Darwin": "/var/"
}

# ================================

COPYRIGHT_START_YEAR = 2023
LAUNCH_TIME = datetime.datetime.now()
OS = platform.system()

CONFIG_FILE_PATH = CONFIG_SAVE_DIR[OS]+CONFIG_FILE_NAME
