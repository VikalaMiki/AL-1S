# python3
# -*- coding: utf-8 -*-
# @Time     : 2022/7/5
# @Author   : Vikala_Miki
# @Email    : Vikala.Miki@gmail.com
# @Github   : https://github.com/VikalaMiki
# @File     : config.py
# @Software : PyCharm
from pydantic import BaseSettings


class Config(BaseSettings):
    # Your Config Here

    class Config:
        extra = "ignore"
