# python3
# -*- coding: utf-8 -*-
# @Time     : 2022/9/29
# @Author   : Vikala_Miki
# @Email    : Vikala.Miki@gmail.com
# @Github   : https://github.com/VikalaMiki
# @File     : approve.py
# @Software : PyCharm
import json
from typing import Optional

from nonebot import logger

from .path import *
from .utils import load


async def group_admin():
    """
    :return : 分群管理json对象
    """
    with open(config_group_admin, mode='r') as f:
        admins_ = f.read()
        admins = json.loads(admins_)
    return admins


async def group_admin_add(gid: str, qq: int) -> Optional[bool]:
    """
    添加分群管理（处理加群请求时接收处理结果）
    :param gid: 群号
    :param qq: qq
    :return: bool
    """
    admins = await group_admin()
    if gid in admins:
        if qq in admins[gid]:
            logger.info(f"{qq}已经是{gid}的分群管理了")
            return False
        else:
            group_admins = admins[gid]
            group_admins.append(qq)
            admins[gid] = group_admins
            with open(config_group_admin, mode='w') as c:
                c.write(str(json.dumps(admins)))
            logger.info(f"群{gid}添加分群管理: {qq}")
            return True
    else:
        logger.info(f"群{gid}首次加入分群管理")
        admins.update({gid: [qq]})
        with open(config_group_admin, mode='w') as c:
            c.write(str(json.dumps(admins)))
        return True


async def group_admin_del(gid: str, qq: int) -> Optional[bool]:
    """
    删除分群管理
    :param gid: 群号
    :param qq: qq
    :return: bool
    """
    admins = await group_admin()
    if gid in admins:
        if qq in admins[gid]:
            logger.info(f"已删除{gid}的分群管理{qq}")
            data = admins[gid]
            data.remove(qq)
            if data:
                admins[gid] = data
            else:
                del (admins[gid])
            with open(config_group_admin, mode='w') as c:
                c.write(str(json.dumps(admins)))
            return True
        else:
            logger.info(f"删除失败: 群{gid}中{qq}还不是分群管理")
            return False
    else:
        logger.info(f"群{gid}还未添加过分群管理")
        return None


async def superuser_on_or_off() -> Optional[bool]:
    admins = await group_admin()
    if admins['su'] == 'False':
        admins['su'] = 'True'
        logger.info('打开超管消息接收')
        with open(config_group_admin, mode='w') as c:
            c.write(str(json.dumps(admins)))
            return True
    else:
        admins['su'] = 'False'
        logger.info('关闭超管消息接收')
        with open(config_group_admin, mode='w') as c:
            c.write(str(json.dumps(admins)))
            return False


async def write_answer(gid: str, answer: str) -> Optional[bool]:
    """
    写入词条
    :param gid: 群号
    :param answer: 词条
    :return: bool
    """
    contents = await load(config_admin)
    if gid in contents:
        data = contents[gid]
        if answer in data:
            logger.info(f"{answer} 已存在于群{gid}的词条中")
            return False
        else:
            data.append(answer)
            contents[gid] = data
            with open(config_admin, mode='w') as c:
                c.write(str(json.dumps(contents)))
            logger.info(f"群{gid}添加入群审批词条: {answer}")
            return True
    else:
        logger.info(f"群{gid}第一次配置此词条: {answer}")
        contents.update({gid: [answer]})
        with open(config_admin, mode='w') as c:
            c.write(str(json.dumps(contents)))
        return True


async def delete_answer(gid: str, answer: str) -> Optional[bool]:
    """
    删除词条
    :param gid: 群号
    :param answer: 词条
    :return: bool
    """
    contents = await load(config_admin)
    if gid in contents:
        if answer in contents[gid]:
            data = contents[gid]
            data.remove(answer)
            if data:
                contents[gid] = data
            else:
                del (contents[gid])
            with open(config_admin, mode='w') as c:
                c.write(str(json.dumps(contents)))
            logger.info(f"群{gid}删除词条: {answer}")
            return True
        else:
            logger.info(f"删除失败, 群{gid}不存在词条: {answer}")
            return False
    else:
        logger.info(f"群{gid}从未配置过词条")
        return None
