# python3
# -*- coding: utf-8 -*-
# @Time     : 2022/7/11
# @Author   : Vikala_Miki
# @Email    : Vikala.Miki@gmail.com
# @Github   : https://github.com/VikalaMiki
# @File     : __init__.py
# @Software : PyCharm
import asyncio
import traceback
from typing import List

from nonebot import on_command
from nonebot.adapters.onebot.v11 import Bot, Message, MessageEvent, GroupMessageEvent
from nonebot.log import logger
from nonebot.matcher import Matcher
from nonebot.params import EventMessage, State, Depends
from nonebot.typing import T_Handler, T_State

from .config import hikari_config, Config
from .hikari_data_source import sources, Source, download_image

options = [source.commands[0] for source in sources]


def get_cid(event: MessageEvent):
    return (
        f"group_{event.group_id}"
        if isinstance(event, GroupMessageEvent)
        else f"private_{event.user_id}"
    )


def get_img_url():
    async def dependency(
            matcher: Matcher,
            event: MessageEvent,
            state: T_State = State(),
            msg: Message = EventMessage(),
    ):
        img_url = ""
        if event.reply:
            if imgs := event.reply.message["image"]:
                img_url = imgs[0].data["url"]
        elif imgs := msg["image"]:
            img_url = imgs[0].data["url"]
        if not img_url:
            matcher.block = False
            await matcher.finish()
        state["img_url"] = img_url

    return Depends(dependency)


def create_matchers():
    def create_handler(source: Source) -> T_Handler:
        async def handler(
                bot: Bot, matcher: Matcher, event: MessageEvent, state: T_State = State()
        ):
            img_url: str = state["img_url"]

            try:
                img = await download_image(img_url)
            except:
                logger.warning(traceback.format_exc())
                await matcher.finish("图片下载出错，请稍后再试")

            try:
                res = await source.func(img)
            except:
                logger.warning(traceback.format_exc())
                await matcher.finish("出错了，请稍后再试")

            help_msg = f"当前搜索引擎：{source.name}\n可使用 {options} 命令使用其他引擎搜索"
            if res:
                await send_msg(bot, event, res, help_msg)
            else:
                await matcher.finish(f"{source.name} 中未找到匹配的图片")

        return handler

    for source in sources:
        on_command(
            source.commands[0],
            aliases=set(source.commands),
            block=True,
            priority=13,
        ).append_handler(create_handler(source), parameterless=[get_img_url()])


create_matchers()


async def handler(
        bot: Bot, matcher: Matcher, event: MessageEvent, state: T_State = State()
):
    img_url: str = state["img_url"]

    try:
        img = await download_image(img_url)
    except:
        logger.warning(traceback.format_exc())
        await matcher.finish("图片下载出错，请稍后再试")

    res: List[Message] = []
    help_msg = ""
    for source in sources:
        try:
            res = await source.func(img)
            if res:
                help_msg = f"当前搜索引擎：{source.name}\n可使用 {options} 命令使用其他引擎搜索"
                break
            else:
                logger.info(f"{source.name} 中未找到匹配的图片")
        except:
            logger.warning(f"{source.name} 搜索出错")

    if not res:
        await matcher.finish("出错了，请稍后再试")

    await send_msg(bot, event, res, help_msg)


on_command("搜图", aliases={"以图搜图", "识图", "搜图", "出自哪里", "找图"}, block=True, priority=13).append_handler(
    handler, parameterless=[get_img_url()]
)


async def send_msg(bot: Bot, event: MessageEvent, msgs: List[Message], help_msg: str):
    msgs = msgs[: hikari_config.hikari_search_max_results]
    msgs.insert(0, Message(help_msg))
    result = await send_forward_msg(bot, event, "天童アリス", bot.self_id, msgs)
    withdraw_time = hikari_config.hikari_search_withdraw
    if withdraw_time:
        message_id = result["message_id"]
        loop = asyncio.get_running_loop()
        loop.call_later(
            withdraw_time,
            lambda: asyncio.ensure_future(bot.delete_msg(message_id=message_id)),
        )


async def send_forward_msg(
        bot: Bot,
        event: MessageEvent,
        name: str,
        uin: str,
        msgs: List[Message],
) -> dict:
    def to_json(msg: Message):
        return {"type": "node", "data": {"name": name, "uin": uin, "content": msg}}

    messages = [to_json(msg) for msg in msgs]
    if isinstance(event, GroupMessageEvent):
        return await bot.call_api(
            "send_group_forward_msg", group_id=event.group_id, messages=messages
        )
    else:
        return await bot.call_api(
            "send_private_forward_msg", user_id=event.user_id, messages=messages
        )
