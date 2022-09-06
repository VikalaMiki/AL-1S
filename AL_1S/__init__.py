from time import sleep

import nonebot
from nonebot.adapters.onebot.v11 import Adapter

from AL_1S.config import InlineGoCQHTTP, RUNTIME_CONFIG


def asgi():
    return nonebot.get_asgi()


def driver():
    return nonebot.get_driver()


def init():
    nonebot.init(**RUNTIME_CONFIG)
    driver().register_adapter(Adapter)
    nonebot.load_plugins("AL_1S/plugins")
    nonebot.load_plugin("nonebot_plugin_moegoe")
    nonebot.load_plugin("nonebot_plugin_petpet")
    if InlineGoCQHTTP.enabled:
        nonebot.load_plugin("nonebot_plugin_gocqhttp")
    # init_database()
    sleep(3)


def run():
    nonebot.run()
