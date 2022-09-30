# python3
# -*- coding: utf-8 -*-
# @Time     : 2022/9/29
# @Author   : Vikala_Miki
# @Email    : Vikala.Miki@gmail.com
# @Github   : https://github.com/VikalaMiki
# @File     : auto_ban_.py
# @Software : PyCharm
from nonebot import on_command
from nonebot.adapters import Message
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot.adapters.onebot.v11.permission import GROUP_ADMIN, GROUP_OWNER
from nonebot.matcher import Matcher
from nonebot.params import CommandArg
from nonebot.permission import SUPERUSER

from AL_1S.plugins.admin.config import plugin_config
from .path import limit_word_path
from .utils import del_txt_line, add_txt_line, get_txt_line

callback_notice = plugin_config.callback_notice

del_custom_limit_words = on_command('删除违禁词', aliases={'移除违禁词', '去除违禁词'}, priority=1,
                                    permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)
# TODO: 支持配置是否撤回&禁言
add_custom_limit_words = on_command('添加违禁词', aliases={'增加违禁词', '新增违禁词'}, priority=1,
                                    permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)

get_custom_limit_words = on_command('查看违禁词', aliases={'查看违禁词', '查询违禁词', '违禁词列表'},
                                    priority=1, permission=GROUP_ADMIN | GROUP_OWNER | SUPERUSER)


@del_custom_limit_words.handle()
async def _(bot: Bot, event: GroupMessageEvent, matcher: Matcher, args: Message = CommandArg()):
    await del_txt_line(limit_word_path, matcher, event, args, '违禁词', False)


@add_custom_limit_words.handle()
async def _(bot: Bot, event: GroupMessageEvent, matcher: Matcher, args: Message = CommandArg()):
    await add_txt_line(limit_word_path, matcher, event, args, '违禁词', False)


@get_custom_limit_words.handle()
async def _(bot: Bot, event: GroupMessageEvent, matcher: Matcher, args: Message = CommandArg()):
    if callback_notice:
        await get_txt_line(limit_word_path, matcher, event, args, '违禁词', False)
