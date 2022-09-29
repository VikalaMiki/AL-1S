# python3
# -*- coding: utf-8 -*-
# @Time     : 2022/9/29
# @Author   : Vikala_Miki
# @Email    : Vikala.Miki@gmail.com
# @Github   : https://github.com/VikalaMiki
# @File     : auto_ban.py
# @Software : PyCharm
import re

from nonebot import on_message, logger
from nonebot.adapters.onebot.v11 import Bot, GroupMessageEvent
from nonebot.exception import ActionFailed
from nonebot.matcher import Matcher

from AL_1S.plugins.admin.path import limit_word_path, time_scop_map
from AL_1S.plugins.admin.utils import get_user_violation, ban_user, sd

forbidden_word = on_message(priority=2, block=False)


@forbidden_word.handle()
async def _(bot: Bot, event: GroupMessageEvent, matcher: Matcher):
    """
    违禁词禁言
    :param bot:
    :param event:
    :return:
    """
    rules = [re.sub(r'\t+', '\t', rule).split('\t') for rule in
             open(limit_word_path, 'r', encoding='utf-8').read().split('\n')]
    msg = re.sub(r'\s', '', str(event.get_message()))
    gid = event.group_id
    uid = event.user_id
    logger.info(f"{gid}收到{uid}的消息: \"{msg}\"")
    for rule in rules:
        if not rule[0]:
            continue
        delete, ban = True, True  # 默认禁言+撤回
        if len(rule) > 1:
            delete, ban = rule[1].find('$撤回') != -1, rule[1].find('$禁言') != -1
            rf = re.search(r'\$(仅限|排除)(([0-9]{6,},?)+)', rule[1])
            if rf:
                chk = rf.groups()
                lst = chk[1].split(',')
                if chk[0] == '仅限':
                    if str(gid) not in lst:
                        continue
                else:
                    if str(gid) in lst:
                        continue
        try:
            if not re.search(rule[0], msg):
                continue
        except:
            if msg.find(rule[0]) == -1:
                continue
        matcher.stop_propagation()  # block
        level = (await get_user_violation(gid, uid, 'Porn', event.raw_message))
        ts: list = time_scop_map[level]
        logger.info(f"敏感词触发: \"{rule[0]}\"")
        if delete:
            try:
                await bot.delete_msg(message_id=event.message_id)
                logger.info('消息已撤回')
            except ActionFailed:
                logger.info('消息撤回失败')
        if ban:
            baning = ban_user(gid, ban_list=[event.get_user_id()], scope=ts)
            async for baned in baning:
                if baned:
                    try:
                        await baned
                        await sd(matcher,
                                 f"你发送了违禁词,现在进行处罚,如有异议请联系管理员\n你的违禁级别为{level}级", True)
                        logger.info(f"禁言成功, 用户: {uid}")
                    except ActionFailed:
                        logger.info('禁言失败, 权限不足')
        break
