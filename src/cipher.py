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


AES_KEY = sha_split_hex(AES_KEY_TEXT, step=8).encode("utf-8")[0:16]
AES_IV = sha_split_hex(AES_IV_TEXT, step=8).encode("utf-8")[0:16]
cipher = AES.new(AES_KEY, AES.MODE_CBC, AES_IV)


def encrypt(username: str, password: str):
    return username + " | " + b64encode(cipher.encrypt(password.encode("utf-8"))).decode("utf-8")


def decrypt(ciphertext: str):
    arr = ciphertext.split(" | ")
    username = arr[0].encode("utf-8")
    password = cipher.decrypt(b64decode(arr[1].encode("utf-8"))).decode("utf-8")
    return (username, password)
