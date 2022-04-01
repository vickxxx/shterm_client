# -*- coding: utf-8 -*-
from Loader import utils
from Loader import logger
from Loader import loader
from Loader import __version__
from Loader import update
import sys
import os

__version__ = __version__


def main():
    shterm_url = sys.argv[1].split("#")[0]
    shterm_data = utils.get_json_from_shterm_url(shterm_url)
    resources_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    loader.get_loader(shterm_data, resources_dir).load()


def test():
    # tui securecrt
    url_scrt = "shterm://eJyrVkosKFCyUipOTS4tSk0uKlHSUSpLLQKKGOkZ6pkCeaHFYG55KZAdnFpcnJmfF5JZkpMKFCvKzy9xeLJj7bNp7c+2dr9YP1XXOTWvJL/Y0EzPyDC+vFRBVyHYI8Q1yBeoNSAfaDbQVCMg2yO/GMQ2NNADIZBiY4ThjsnJ+aV5JVDjEeJ+ibkgO/FYB1RbWpQDVJNRUlJQbKWvj2yBlYmJsX5xRklqUa5+UWpxfmlRcmqxfnJ+Xpp+MFjUOScTaJpeakUqwk5MhwLlQhKTQGJAFsS4eGh4gTwZ7gJk+YcEWFkGeriZOEVkuQXlmCnVAgCQ8XTp"
    # gui
    url_mstsc = "shterm://eJxdUstOw0AM/JVVzpCkaXnlREEIJCgg2gsntM0asuq+WDs8xb/jTaoUIe3FHo/tGe93JkPI6swiYZPtZW8QOaryST7lSHbUgiPdSNLeCQNvYBjWdcUgOLk20ERQiAG7EHykHiwZfO6MEVKpCIicxHpS5ukd5lWZyEvOc8uVJgOMS2W100hRko+nXDUpj/e/PsW+WF6tLh4WzFCAG/KhBf3SDnO4Jo3CoZVY90I4fbjrP28a3zn6PyGxeHFwwnoFQquBuOPdSpvWGhdhpItJeksUsC6Kv3Lq2WxaYEsQbcF6fRcbwKLx7rlY9tlzo9nFHD6A+1j5oa3+6tsniw1XOEkgsAVjeq+W5fXt6nLyeDy/PDhbiLvVfb2oJFav7/P79dENsyJYT8CnM9vbJB2j+SF6GyhdJh1PGu+aHbhVeOUx2TLqYJ0MbuBz7WVUrfeb0ZOt8+9aUTskT6qy/x1K+3FwuupgwtP2E2U/v7zAv8M="
    # gui playback
    url_guiplayer = "shterm://eJxNjUELgkAQhf/LnmNX0yL3mktF6EpKRJewbUTJVNZViui/N1sdgmF435vHmyfJu45wshqqpM4foMmEjLg5mVKXekiJ3GWIs0UQIEUyFEgdZs+5uqKzlqm9uw61M6dTx0e3Lw3o2+lXZQ1QgwYbRMjkVsSoZZbwehQQu0dTHS4RnsRexLavLQqkQdeoS2O6njP2/4P7vse+X5iGvh20gp6ptilY+nGXdQWNoXAH7Ek3IfY45PUGGTxEbQ=="
    # batch
    url_batch = "shterm://eJxNT8tqwzAQ/JWicy1ZsvzAEIrjytBLe9A1YFRpg00Sy0hKKJT+eyUnhcIednd2dma+0Q0cahHDFBfoGc1+/FRBT3FF47haF2LLecKuHkbvzw9osj5BNMepKsxouplAme1hb+1phvZJCinfPt53Q/Vad40o9x1lZd7VfBC84P3Qi6ERvOQHd1gi308B3GV8mEqiLglOIay+JeS/Whtdkfs9ceDt1WnwRNvlSOS27c8zLAHDF9z/jKsKKdgfSa0zMXCbNXQ6Uj3ZksugXHgJ9gTLrlaMATuqLAejMm50lTVAi8xo02jFqxoKg35+AZBZYXA="
    #Terminal
    url_terminal = "shterm://eJyFkMtOwzAQRX+l8hqs2G5C0xUqQu2Cl2ip2LrOqLGIH8ROogjx752RKrFkd+743nn4h7WerZkeGpvbkDJPcwqOhwieGwTj2Q2LZJESyUSk7UasClWgnDLKPaRkA/nAj6gRBgp0Vvtz6yg/oXw9vIn1i/SfR/fxdHyApqQGiYyn0ZeVHmRYQq6sMN/1l6zh5O7QkVuavSSiLisam6i9cbGzXipVUYVcouB1yaWSXBSCihqL8zRPxPnK93+5xe1ivzs8vj/juwsNoKOxPZiMWke61GboHd09Qk9rcMVpk6Hv/vmz3wuNFGTQ"

    shterm_urls = [url_terminal]#, url_mstsc, url_guiplayer, url_batch, url_terminal]
    for shterm_url in shterm_urls:
        shterm_data = utils.get_json_from_shterm_url(shterm_url)
        logger.logger.debug("shterm_data: " + str(shterm_data))
        resources_dir = "."
        try:
            loader.get_loader(shterm_data, resources_dir).load()
        except Exception as e:
            logger.logger.exception(e)
        from time import sleep
        sleep(1)

if __name__ == "__main__":
    test()
