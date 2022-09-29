# python3
# -*- coding: utf-8 -*-
# @Time     : 2022/9/7
# @Author   : Vikala_Miki
# @Email    : Vikala.Miki@gmail.com
# @Github   : https://github.com/VikalaMiki
# @File     : config.py
# @Software : PyCharm
from nonebot import get_driver
from pydantic import BaseModel, Extra

from . import utils


class Config(BaseModel, extra=Extra.ignore):
    tencent_id: str = ''
    tencent_keys: str = ''
    callback_notice: bool = True
    ban_rand_time_min: int = 60
    ban_rand_time_max: int = 2591999


driver = get_driver()
global_config = driver.config
plugin_config = Config.parse_obj(global_config)


@driver.on_bot_connect
async def _():
    await utils.init()
