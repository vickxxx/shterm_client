# -*- coding: utf-8 -*-
from .logger import logger
from . import utils
from . import template_file
import datetime
import subprocess
import os
import json
import tempfile
import ssl
import multiprocessing
import re
import sys
try:
    from urllib.request import Request, urlopen
except ImportError:
    from urllib2 import Request, urlopen

lock = multiprocessing.Lock()


class Loader(object):
    conf_file_path = conf_dir = os.path.join(
        os.path.expanduser("~"),
        ".local",
        "shterm_client.conf"
    )

    def __init__(self, shterm_data, resources_dir):
        self.shterm_data = shterm_data
        self.resources_dir = resources_dir
        self.init_conf_file()

    def get_sessiontitle(self):
        device_name = self.shterm_data.get("SessionName")
        device_address = self.shterm_data.get("SessionHost")
        session_account = self.shterm_data.get("SessionAccount")
        session_title = self.shterm_data.get("SessionTitle")

        if not session_title:
            session_title = session_account
            if device_name:
                session_title += "@" + device_name
            else:
                session_title = device_name
            if device_address > 0:
                session_title += "({0})".format(device_address)
        elif device_address:
            if session_account:
                session_title += "@" + device_address
            else:
                session_title = device_address
        return session_title

    def get_choose_app(self):
        return self.shterm_data["app"]

    def find_application(self):
        file_path = self.find_application_conf()
        if file_path and utils.exist_and_executable(file_path):
            return file_path

        logger.warning("invalid filepath in shterm_client.conf: ({app}: {filepath})"
                       .format(app=self.shterm_data["app"], filepath=file_path))

        if not file_path:
            file_path = self.find_application_normal()

        if not utils.exist_and_executable(file_path):
            logger.warning("not exists or executable: {0}".format(file_path))
            file_path = None

        if not file_path:
            choose_app = self.get_choose_app()
            file_path = self.find_application_locate(choose_app=choose_app)

        if not utils.exist_and_executable(file_path):
            logger.warning("not exists or executable: {0}".format(file_path))

        self.save_application(file_path)
        return file_path

    def find_application_conf(self):
        with open(Loader.conf_file_path, "r") as f:
            try:
                conf = json.load(f)
            except ValueError as e:
                logger.warning(e)
                return None
            return conf["app"].get(self.shterm_data["app"])

    def find_application_normal(self):
        pass

    def find_application_locate(self, choose_app):
        file_path = self.open_filedialog(title="please choose file: " + choose_app)
        return file_path

    def open_filedialog(self, title=""):
        return utils.askopenfilename(title)

    def init_conf_file(self):
        conf_dir, conf_file = os.path.split(Loader.conf_file_path)

        if not os.path.exists(conf_dir):
            os.makedirs(conf_dir)

        if not os.path.exists(Loader.conf_file_path):
            with lock:
                with open(Loader.conf_file_path, "w") as f:
                    json.dump({"app": {}}, f, indent=4)

    def save_application(self, file_path):
        with lock:
            with open(Loader.conf_file_path, "r+") as f:
                try:
                    conf = json.load(f)
                except ValueError as e:
                    logger.warning(e)
                    conf = {"app": {}}
            with open(Loader.conf_file_path, "w") as f:
                conf["app"][self.shterm_data["app"]] = file_path
                json.dump(conf, f, indent=4)

    def get_cmdline(self):
        cmdline = [self.find_application()]
        cmdline.extend(self.get_cmdline_args() or [])
        return cmdline

    def get_cmdline_args(self):
        pass

    def load_post_process(self):
        pass

    def load(self):
        cmdline = self.get_cmdline()
        try:
            cmdline = [unicode(x).encode(sys.getfilesystemencoding())
                       for x in cmdline]
        except NameError:
            cmdline = [str(x) for x in cmdline]
        logger.info(" ".join(cmdline))
        subprocess.Popen(cmdline)
        self.load_post_process()


class MstscLoader(Loader):
    def get_cmdline_args(self):
        cmdline_args = []
        self.cfg_file = self.generate_mstsc_cfg()
        cmdline_args.append(self.cfg_file)
        return cmdline_args

    def generate_mstsc_cfg(self):
        screen_mode_id = self.shterm_data.get("screen mode id")[2:]  # 1: window mode 2: fullscreen
        bpp = self.shterm_data.get("session bpp", "i:16")[2:]
        enable_cred_ssp_support = self.shterm_data.get("enablecredsspsupport", "i:0")[2:]
        maximize = self.shterm_data.get("maximize")
        width = self.shterm_data.get("desktopwidth", "i:800")[2:]
        height = self.shterm_data.get("desktopheight", "i:600")[2:]
        drive_redirection_mode = self.shterm_data.get("drive_redirection_mode", 0)
        redirect_folder = self.shterm_data.get("redirect_folder", "/Users")

        context = {
            "DesktopSize": None,
            "DriveRedirectionMode": drive_redirection_mode,
            "RedirectFolder": redirect_folder
        }

        if screen_mode_id == "2" or maximize == 1:
            context["DesktopSize"] = template_file.fullscreen_desktopsize
        else:
            context["DesktopSize"] = template_file.dict_desktopsize.format(width=width, height=height)

        keys = {
            "alternate shell": "ApplicationPath",
            "full address": "ConnectionString",
            "audiomode": "AudioRedirectionMode",
        }

        for k, v in keys.items():
            context[v] = self.shterm_data.get(k)[2:]

        template_str = template_file.rdc_cfg_tmpl.format(**context)

        suffix = ".rdp"
        handle, cfg_file = tempfile.mkstemp(suffix=suffix)
        with os.fdopen(handle, "w") as f:
            f.write(template_str)
        return cfg_file

    def get_choose_app(self):
        return "Remote Desktop Connection"

    def find_application_normal(self):
        return "/Applications/Remote Desktop Connection.app/Contents/MacOS/Remote Desktop Connection"

    def load_post_process(self):
        utils.run_files_cleaner([self.cfg_file], 10)


class SecurecrtLoader(Loader):
    def get_cmdline_args(self):
        if self.shterm_data['app'] == 'scrt':
            return self.get_other_mode_cmdline_args()
        else:
            return self.get_access_cmdline_args()

    def get_other_mode_cmdline_args(self):
        cmdline_args = []
        cmdline_args.append("/T")
        cmdline_args.append("/ssh2")
        cmdline_args.append(self.shterm_data.get("hn"))
        cmdline_args.append("/P")
        cmdline_args.append(self.shterm_data.get("pn"))
        cmdline_args.append("/L")
        cmdline_args.append(self.shterm_data.get("un"))
        cmdline_args.append("/PASSWORD")
        cmdline_args.append(self.shterm_data.get("pw"))
        return cmdline_args

    def get_access_cmdline_args(self):
        cmdline_args = []
        if self.shterm_data.get("Tab"):
            cmdline_args.append("/T")
        session_title = self.get_sessiontitle()
        session_title = re.sub(r'"', r'\"', session_title)
        if session_title:
            cmdline_args.append("/N")
            cmdline_args.append(session_title)
            cmdline_args.append("/TITLEBAR")
            cmdline_args.append(session_title)
        cmdline_args.append("/ssh2")
        cmdline_args.append(self.shterm_data.get("Host"))
        cmdline_args.append("/P")
        cmdline_args.append(self.shterm_data.get("Port"))
        cmdline_args.append("/L")
        cmdline_args.append(self.shterm_data.get("User"))
        cmdline_args.append("/PASSWORD")
        cmdline_args.append(self.shterm_data.get("PWD"))

        return cmdline_args

    def get_choose_app(self):
        return "SecureCRT"

    def find_application_normal(self):
        return "/Applications/SecureCRT.app/Contents/MacOS/SecureCRT"


class GuiPlayerLoader(Loader):
    def get_cmdline_args(self):
        jar_path = r"{path}".format(path=os.path.join(self.resources_dir, "GuiPlayer.jar"))
        cmdline_args = ["-Dfile.encoding=utf-8", "-Xms8m", "-Xmx128m", "-cp",
                        jar_path, "GuiPlayer"]

        logger.debug(self.shterm_data)
        keys = [
            "EVENT",
            "HOST",
            "MODE",
            "PORT",
            "SID",
            "TOKEN",
            "SECURE",
            "SEEK",
            "THUMB",
            "EVENT",
            "ACTION",
            "REWIND"
        ]
        for k, v in self.shterm_data.items():
            if k.upper() in keys:
                cmdline_args.append(k)
                cmdline_args.append(v)

        cmdline_args.append("REDIRECTFILE")
        suffix = "guiplayer-{0}.log".format(datetime.datetime.now().strftime("%Y-%m-%d"))
        handle, redirect_filepath = tempfile.mkstemp(suffix=suffix)
        os.close(handle)
        cmdline_args.append(redirect_filepath)
        return cmdline_args

    def get_choose_app(self):
        return "java"

    def find_application_normal(self):
        return utils.which("java")


class GuiViewerLoader(Loader):
    def get_cmdline_args(self):
        jar_path = r"{path}".format(path=os.path.join(self.resources_dir, "GuiViewer.jar"))
        cmdline_args = ["-Dfile.encoding=utf-8", "-Xms8m", "-Xmx128m", "-cp",
                        jar_path, "GuiViewer"]

        logger.debug(self.shterm_data)
        keys = [
            "EVENT",
            "HOST",
            "MODE",
            "PORT",
            "SID",
            "TOKEN",
            "SECURE",
            "CLIENTTEXTLIMIT",
            "CLIPENCODE"
        ]
        for k, v in self.shterm_data.items():
            if k.upper() in keys:
                cmdline_args.append(k)
                cmdline_args.append(v)

        cmdline_args.append("REDIRECTFILE")
        suffix = "guiplayer-{0}.log".format(datetime.datetime.now().strftime("%Y-%m-%d"))
        handle, redirect_filepath = tempfile.mkstemp(suffix=suffix)
        os.close(handle)
        cmdline_args.append(redirect_filepath)
        return cmdline_args

    def get_choose_app(self):
        return "java"

    def find_application_normal(self):
        return utils.which("java")


class BatchLoader(object):
    def __init__(self, shterm_data, resources_dir):
        self.shterm_data = shterm_data
        self.resources_dir = resources_dir

    def make_url(self):
        return self.shterm_data["batch_url"]

    def parse_headers(self, header_str):
        return [
            line.split(': ', 1)
            for line in header_str.split("\r\n") if line != ""
        ]

    def get_batch_data(self):
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        url = self.make_url()
        logger.debug("batch url: " + url)
        req = Request(url)

        if "header" in self.shterm_data:
            for header in self.parse_headers(self.shterm_data["header"]):
                logger.debug(header)
                req.add_header(header[0], header[1])

        return urlopen(req, context=ctx, timeout=10).read().decode("utf-8")

    def load(self):
        batch_data = self.get_batch_data()
        logger.debug("batch_data: " + batch_data)
        for shterm_url in json.loads(batch_data):
            shterm_data = utils.get_json_from_shterm_url(shterm_url)
            get_loader(shterm_data, self.resources_dir).load()


class TerminalLoader(Loader):
    def generate_expect_file(self):
        suffix = ".command"
        handle, expect_file = tempfile.mkstemp(suffix=suffix)
        # escape user, host, port, pwd for variable in expect script
        user = re.escape(self.shterm_data.get("un"))
        host = re.escape(self.shterm_data.get("hn"))
        port = re.escape(self.shterm_data.get("pn"))
        pwd = re.escape(self.shterm_data.get("pw"))
        terminal_expect = template_file.terminal_expect.format(user=user, host=host, port=port, password=pwd)
        with os.fdopen(handle, "w") as f:
            f.write(terminal_expect)
        os.chmod(expect_file, 0o777)
        return expect_file

    def get_cmdline_args(self):
        cmdline_args = []
        self.expect_file = self.generate_expect_file()
        cmdline_args.append(self.expect_file)
        return cmdline_args

    def get_choose_app(self):
        return "open"

    def find_application_normal(self):
        return utils.which("open")

    def load_post_process(self):
        utils.run_files_cleaner([self.expect_file], 10)


class ITerm2Loader(Loader):
    def get_cmdline_args(self):
        cmdline_args = []

        user = self.shterm_data.get("un")
        host = self.shterm_data.get("hn")
        port = self.shterm_data.get("pn")
        pwd = self.shterm_data.get("pw")

        cmdline_args.append(os.path.join(self.resources_dir, "Scripts", "iterm2_loader.scpt"))
        iterm2_cmd = "ssh -p {port} -o StrictHostKeyChecking=no {user}@{host}".format(
            port=port,
            user=user,
            host=host
        )
        cmdline_args.append(iterm2_cmd)
        cmdline_args.append(pwd)
        cmdline_args.append(self.shterm_data.get("tab", "1"))
        return cmdline_args

    def get_choose_app(self):
        return "osascript"

    def find_application_normal(self):
        return utils.which("osascript")

    def load(self):
        cmdline = self.get_cmdline()
        try:
            cmdline = [unicode(x).encode(sys.getfilesystemencoding())
                       for x in cmdline]
        except NameError:
            cmdline = [str(x) for x in cmdline]
        logger.info(" ".join(cmdline))
        p = subprocess.Popen(cmdline)
        p.wait()
        self.load_post_process()


class FileZillaLoader(Loader):
    def get_cmdline_args(self):
        # filezilla [protocol://][user[:pass]@]host[:port][/path]

        keys = [
            "USER",
            "HOST",
            "PORT",
            "PATH",
            "PWD",
            "PROTO"
        ]

        data = {}
        for k, v in self.shterm_data.items():
            if k.upper() in keys:
                data[k.upper()] = v

        arg = "{proto}://{user}:{pwd}@{host}".format(
            proto=data.get("PROTO") or "sftp",
            user=data.get("USER"),
            pwd=data.get("PWD"),
            host=data.get("HOST")
        )

        if "PORT" in data:
            arg += ":" + data["PORT"]

        if "PATH" in data:
            arg += "/" + data["PATH"]

        return [arg]

    def get_choose_app(self):
        return "FileZilla"

    def find_application_normal(self):
        return "/Applications/FileZilla.app/Contents/MacOS/filezilla"


def get_loader(shterm_data, resources_dir):
    table = {
        "mstsc": MstscLoader,
        "securecrt": SecurecrtLoader,
        "scrt": SecurecrtLoader,
        "GuiPlayer": GuiPlayerLoader,
        "GuiViewer": GuiViewerLoader,
        "Terminal": TerminalLoader,
        "filezilla": FileZillaLoader,
        "iTerm2": ITerm2Loader
    }

    tmp = {}
    for k, v in table.items():
        tmp[k] = v
        tmp[k.lower()] = v
    table = tmp

    if shterm_data.get("batch_url"):
        return BatchLoader(shterm_data, resources_dir)

    if shterm_data["app"] not in table:
        logger.warning("not supported app: " + shterm_data["app"])
    return table[shterm_data["app"]](shterm_data, resources_dir)


def test():
    shterm_data = {u'SessionHost': u'10.10.16.21', u'SessionTitle': u'root@10.10.16.21-wu - SHTERM', u'ver': u'2.1.3',
                   u'Tab': u'1', u'url': u'https://10.10.16.202:443/shterm/resources/conf/ShtermClient.exe',
                   u'app': u'Terminal', u'PWD': u'OTP:XrtZURRFuL2s', u'SessionAccount': u'root',
                   u'Host': u'10.10.16.202', u'User': u'aa0`~@#$%&*()=[]\\;\',/+{}|:"<>?',
                   u'SessionName': u'10.10.16.21-wu', u'shterm_ver': u'2', u'Port': u'22'}
    # shterm_data = {u'desktopwidth': u'i:1920', u'alternate shell': u's:S14WPDQTRP5IF5 OTP:28hoDydkHg1V', u'maximize': u'1', u'promptcredentialonce': u'i:0', u'app': u'mstsc', u'session bpp': u'i:16', u'SessionAccount': u'administrator', u'SessionName': u'16.108-zy', u'keyboardhook': u'i:1', u'shterm_ver': u'2', u'SessionHost': u'10.10.16.108', u'ver': u'2.1.3', u'screen mode id': u'i:1', u'desktopheight': u'i:1200', u'audiomode': u'i:2', u'full address': u's:10.10.16.202', u'authentication level': u'i:2', u'enablecredsspsupport': u'i:0', u'drivestoredirect': u's:c:;d:;e:;', u'redirectdrives': u'i:1', u'console': u'true', u'remoteapplicationmode': u'i:0', u'SessionTitle': u'administrator@16.108-zy - SHTERM', u'url': u'https://10.10.16.202:443/shterm/resources/conf/ShtermClient.exe'}
    loader = get_loader(shterm_data, ".")
    loader.load()


if __name__ == "__main__":
    test()
