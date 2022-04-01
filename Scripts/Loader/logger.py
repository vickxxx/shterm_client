# -*- coding: utf-8 -*-
from . import __version__
import logging
from logging.handlers import RotatingFileHandler
import tempfile
import os

logger = logging.getLogger("ShtermClient")
formatter = logging.Formatter('[%(asctime)s] [{v}] [%(levelname)s] [%(filename)s: %(lineno)d %(funcName)s] %(message)s'
                              .format(v=__version__))
file_handler = RotatingFileHandler(os.path.join(tempfile.gettempdir(), "shterm_client.log"),
                                   maxBytes=8*1024*1024, backupCount=2)
file_handler.setFormatter(formatter)
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)
