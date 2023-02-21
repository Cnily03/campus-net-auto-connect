import os
import shutil

PROGRAM_NAME = "AutoConnect"

logo_path = os.path.abspath('./logo.ico')
options = {
    "single_file": True,
    "no_console": False,
    "ignore_error": True
}

command = ' '.join([i for i in [
    "pyinstaller",
    "-F" if options["single_file"] else ''
    "-w" if options["no_console"] else '',
    "-i" if options["ignore_error"] else '',
    logo_path,
    "-n {}".format(PROGRAM_NAME),
    "./__main__.py"
] if i])

os.system(command)

for fn in os.listdir("./"):
    if fn == "build":
        shutil.rmtree("build")
    if fn.endswith(".spec"):
        os.remove(fn)
