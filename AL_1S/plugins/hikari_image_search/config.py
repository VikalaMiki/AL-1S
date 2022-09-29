# python3
# -*- coding: utf-8 -*-
# @Time     : 2022/7/11
# @Author   : Vikala_Miki
# @Email    : Vikala.Miki@gmail.com
# @Github   : https://github.com/VikalaMiki
# @File     : config.py
# @Software : PyCharm
from nonebot import get_driver
from pydantic import BaseModel, Extra

from AL_1S.config import HikariImageSearch


class Config(BaseModel, extra=Extra.ignore):
    hikari_search_api: str = HikariImageSearch.hikari_search_api
    hikari_search_max_results: int = HikariImageSearch.hikari_search_max_results
    hikari_search_withdraw: int = HikariImageSearch.hikari_search_withdraw


hikari_config = Config.parse_obj(get_driver().config.dict())
