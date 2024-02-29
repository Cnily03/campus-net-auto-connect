import random
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
import hashlib
from config import *


def sha_split_hex(string, step=16):
    hex = hashlib.sha256(string.encode("utf-8")).hexdigest()
    result = ''
    for start in range(0, step):
        for i in range(start, len(hex), step):
            result += hex[i]
    return result


alphabet = "abcdefghijklmnopqrstuwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789?!@#$%^&()_+*-/=[]{}|\\,.<>:\";'`~* "


def pad(src: bytes, length: int, pad_char: bytes = None, mode="end"):
    pad_count = length - len(src) % length

    # force strech
    if pad_count < 3:
        pad_count += length

    pad_str = bytes([ord(alphabet[random.randrange(0, len(alphabet), 1)] if pad_char == None else pad_str[:1])
                     for i in range(pad_count)])

    result = b''
    start = 0
    if mode == "between":
        start = random.randrange(1, len(pad_str)-1, 1)
    elif mode == "start":
        start = 0

    result = pad_str[:start] + src + pad_str[start:]

    return (result, start)


def depad(src, start=0):
    return src[start:len(src)-start]


AES_KEY = sha_split_hex(AES_KEY_TEXT, step=8).encode("utf-8")[0:16]
AES_IV = sha_split_hex(AES_IV_TEXT, step=8).encode("utf-8")[0:16]
cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)

SPLITER = " | "


def encrypt(username: str, password: str):
    passwd_padded, pad_start = pad(password.encode("utf-8"), length=16, mode="between")
    pad_start_padded, __ = pad((" " + str(pad_start) + " ").encode("utf-8"),
                               length=16, mode="between")
    return SPLITER.join(
        [username,
         b64encode(cipher.encrypt(passwd_padded)).decode("utf-8"),
         b64encode(cipher.encrypt(pad_start_padded)).decode("utf-8")])


def decrypt(ciphertext: str):
    arr = ciphertext.split(SPLITER)
    username = arr[0].encode("utf-8")

    passwd_padded = cipher.decrypt(b64decode(arr[1].encode("utf-8"))).decode("utf-8")
    pad_start = int(cipher.decrypt(b64decode(arr[2].encode("utf-8")))
                    .decode("utf-8").split(" ")[1].strip())
    password = depad(passwd_padded, pad_start)
    return (username, password)
