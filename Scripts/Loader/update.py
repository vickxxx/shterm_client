# -*- coding: utf-8 -*-
import zipfile
import re
import os
import sys
from .logger import logger
from . import __version__
from . import utils
try:
    from urllib.request import Request, urlopen
except ImportError:
    from urllib2 import Request, urlopen
import ssl

progress = {}


def download_file(url, filepath):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    req = Request(url)
    res = urlopen(req, context=ctx, timeout=10)
    size = int(res.headers.getheader("Content-Length", 0))
    progress["size"] = size
    progress["downloaded"] = 0
    chunk_size = 65536

    with open(filepath, "wb") as f:
        while True:
            chunk = res.read(chunk_size)
            if not chunk:
                break
            f.write(chunk)
            progress["downloaded"] += len(chunk)
            logger.debug(progress)


def get_version_value(ver):
    if not ver:
        return 0
    val = 0
    for x in map(lambda _: int(_), ver.split(r".")):
        val += x
        val *= 256
    return val


def get_version(url):
    filename = "ShtermClient.app.zip"
    try:
        download_file(url, filename)
        with zipfile.ZipFile(filename, "r") as f:
            ver = f.open("ShtermClient.app/Contents/Resources/Scripts/Loader/__init__.py").read()
            match = re.search(r"\d+.\d+.\d+.\d", ver)
            if match:
                ver = match.group(0)
        os.remove(filename)
    except Exception as e:
        logger.warn(e)
        return None
    logger.info("get version [%s] from: %s" % (ver, url))
    return ver


def check_update(host, port, server_version):
    download_url = get_update_url(host, port)
    if not server_version:
        return False
    if get_version_value(__version__) < get_version_value(server_version):
        decision = utils.askyesno("Update", "发现新版本，是否更新?")
        if decision:
            utils.openbrowser(download_url)
            return True
    return False


def get_update_url(host, port):
    return "https://{host}:{port}/shterm/resources/conf/ShtermClient.app.zip".format(host=host, port=port)


