import os
import shutil
import sys

PROGRAM_NAME = "AutoConnect"
directories = ["./src"]
extensions = [".py"]
files = ["config.py"]
modules = ["json", "requests", "tkinter", "tkinter.messagebox",
           "platform", "maskpass", "Crypto.Cipher.AES"]

options = {
    "onefile": True,
    "noconsole": False,
    "icon": os.path.abspath('./logo.ico'),
    "filename": PROGRAM_NAME
}

print("Generating requirements.txt ...")
os.system("pipreqs ./ --encoding=utf8 --force")

# --add-data

data = []
for _root, _dirs, _files in os.walk("./src"):
    for fn in _files:
        if True in [fn.endswith(ext) for ext in extensions]:
            data.append((_root+'/'+fn, _root))

for file in files:
    src = "./"+os.path.relpath(file, ".")
    dst = "./"+os.path.relpath(os.path.dirname(os.path.abspath(file)), ".")
    dst = "." if dst == "./." else dst
    data.append((src, dst))

command = ' '.join([i for i in [
    "pyinstaller",
    "--clean",
    "-F" if options["onefile"] else ''
    "-w" if options["noconsole"] else '',
    "-i {}".format(options["icon"]),
    "-n {}".format(options["filename"]),
    " ".join(["--add-data \""+";".join([_src, _dst])+"\"" for _src, _dst in data]),  # --add-data
    " ".join(["--hidden-import "+_module for _module in modules]),  # --hidden-import
    "./__main__.py"
] if i])

[(os.remove("./dist/"+fn) if os.path.isfile("./dist/"+fn) else shutil.rmtree("./dist/"+fn))
 for fn in os.listdir("./dist")] if os.path.exists("./dist") else None
os.system(command)

# for fn in os.listdir("./"):
#     if fn == "build":
#         shutil.rmtree("build")
#     if fn.endswith(".spec"):
#         os.remove(fn)
