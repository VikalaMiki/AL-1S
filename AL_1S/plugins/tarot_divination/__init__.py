# python3
# -*- coding: utf-8 -*-
# @Time     : 2022/6/19
# @Author   : Vikala_Miki
# @Email    : Vikala.Miki@gmail.com
# @Github   : https://github.com/VikalaMiki
# @File     : __init__.py
# @Software : PyCharm
from typing import List, Dict, Union

from nonebot import on_command, on_regex
from nonebot.adapters.onebot.v11 import Bot, MessageSegment, PrivateMessageEvent, GroupMessageEvent
from nonebot.adapters.onebot.v11.event import MessageEvent
from nonebot.matcher import Matcher
from nonebot.permission import SUPERUSER

from .config import tarot_config
from .tarot_data_source import tarot_manager

divine = on_command(cmd="divine", aliases={"占卜", "塔罗牌占卜"}, priority=7)
tarot = on_command(cmd="tarot", aliases={"塔罗牌", "单张塔罗牌"}, priority=7)
chain_reply_switch = on_regex(pattern=r"(开启|启用|关闭|禁用)群聊转发", permission=SUPERUSER, priority=7, block=True)


@divine.handle()
async def _(bot: Bot, event: MessageEvent):
    # 发送牌阵
    msg, cards_num = await tarot_manager.divine()
    await divine.send(msg)

    chain = []
    for i in range(cards_num):
        reveal_msg = await tarot_manager.reveal(i)

        if isinstance(event, PrivateMessageEvent):
            if i < cards_num:
                await divine.send(reveal_msg)
            else:
                await divine.finish(reveal_msg)

        if isinstance(event, GroupMessageEvent):
            if not tarot_manager.is_chain_reply:
                # 开启群聊转发模式
                if i < cards_num - 1:
                    await divine.send(reveal_msg)
                else:
                    await divine.finish(reveal_msg)
            else:
                chain = await chain_reply(bot, chain, reveal_msg)

    if tarot_manager.is_chain_reply:
        await bot.send_group_forward_msg(group_id=event.group_id, messages=chain)


@tarot.handle()
async def _(matcher: Matcher):
    msg = await tarot_manager.single_divine()
    await matcher.finish(msg)


@chain_reply_switch.handle()
async def _(event: GroupMessageEvent):
    args = event.get_plaintext()
    msg = []
    if args[:2] == "开启" or args[:2] == "启用":
        tarot_manager.switch_chain_reply(True)
        msg = "占卜群聊转发模式已开启~"
    elif args[:2] == "关闭" or args[:2] == "禁用":
        tarot_manager.switch_chain_reply(False)
        msg = "占卜群聊转发模式已关闭~"

    await chain_reply_switch.finish(msg)


async def chain_reply(bot: Bot, chain: List[Dict[str, Union[str, Dict[str, Union[str, MessageSegment]]]]],
                      msg: MessageSegment) -> List[Dict[str, Union[str, Dict[str, Union[str, MessageSegment]]]]]:
    data = {
        "type": "node",
        "data": {
            "name": f"{list(tarot_config.nickname)[0]}",
            "uin": f"{bot.self_id}",
            "content": msg
        },
    }
    chain.append(data)
    return chain
