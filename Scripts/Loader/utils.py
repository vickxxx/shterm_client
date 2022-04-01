# -*- coding: utf-8 -*-
from .logger import logger
import sys
import base64
import zlib
import json
import os
import threading
import time
import re
import webbrowser
import functools
try:
    import Tkinter as tk
    import tkFileDialog as filedialog
    import tkMessageBox as messagebox
except ImportError:
    import tkinter as tk
    from tkinter import filedialog, messagebox

__author__ = 'logeable'

schema = "shterm://"


def get_shterm_url():
    logger.debug("get_shterm_url: " + sys.argv[1])
    return sys.argv[1]


def decode_shterm_url(shterm_url):
    logger.debug("decode_shterm_url: " + shterm_url)
    b64_str = shterm_url[len(schema):]
    return base64.b64decode(b64_str)


def decompress_zlib_data(zlib_data):
    logger.debug("decompress_zlib_data: ")
    return zlib.decompress(zlib_data)


def get_json_from_shterm_url(shterm_url):
    logger.info("shterm_url: " + shterm_url)
    return json.loads(decompress_zlib_data(decode_shterm_url(shterm_url)).decode("utf-8"))


def which(app):
    splitter = ":"
    import sys
    if sys.platform.startswith("win"):
        splitter = ";"
        if not os.path.splitext(app)[1].strip():
            app += ".exe"
    paths = os.environ["PATH"].split(splitter)
    for path in paths:
        if path.strip():
            if app in os.listdir(path):
                return os.path.join(path, app)


def exist_and_executable(filepath):
    return filepath and os.path.exists(filepath) and os.access(filepath, os.X_OK)


def generate_file(path, content, mode=0o644):
    if os.path.exists(path):
        logger.info("{path} already exist".format(path=path))
        return
    with open(path, "w") as f:
        f.write(content)
    os.chmod(path, mode)


def run_files_cleaner(files, delay=5):
    assert isinstance(files, (list, tuple))

    def clean_func():
        time.sleep(delay)
        map(os.remove, files)
    threading.Thread(target=clean_func).start()


def get_host_port_from_url(url):
    match = re.search(r"http[s]?://(\d+.\d+.\d+.\d+):(\d+)/", url)
    return match.groups()


def tk_context(func):

    @functools.wraps(func)
    def wrap(*args, **kwargs):
        root = tk.Tk()
        root.withdraw()

        ret = func(*args, **kwargs)

        root.destroy()
        return ret

    return wrap


@tk_context
def showinfo(title, content):
    messagebox.showinfo(title, content)


@tk_context
def askyesno(title, content):
    return messagebox.askyesno(title, content)


@tk_context
def askopenfilename(title):
    return filedialog.askopenfilename(title=title)


def openbrowser(url):
    webbrowser.open(url)


if __name__ == "__main__":
    assert which("java")
