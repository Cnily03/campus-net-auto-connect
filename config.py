import datetime
from os import getenv
import platform

# ================================

PROGRAM_NAME = "AutoConnect"
__version__ = "1.0.0"
CONFIG_FILE_NAME = ".compusnetinfo"

AES_KEY_TEXT = "随便乱输一段文字"
AES_IV_TEXT = "随便乱输一段文字"

CONFIG_SAVE_DIR = {
    "Windows": "{}/".format(getenv("APPDATA")),
    "Linux": "/{}/".format(getenv("HOME")),
    "Darwin": "/var/"
}
# ================================

LAUNCH_TIME = datetime.datetime.now()
OS = platform.system()

CONFIG_FILE_PATH = CONFIG_SAVE_DIR[OS]+CONFIG_FILE_NAME
