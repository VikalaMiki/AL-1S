import os

from nonebot import get_driver, get_bot
from nonebot.adapters.onebot.v11 import Bot, MessageEvent, GroupMessageEvent
from nonebot.matcher import Matcher
from nonebot.plugin import on_startswith
from nonebot.rule import Rule

from .cards import _cachepath, cards, cache_cards, set_handler, show_handler, sa_handler, del_handler
from .dices import rd, help_message, st, en
from .investigator import Investigator
from .madness import ti, li
from .san_check import sc

driver = get_driver()


@driver.on_startup
async def _():  # 角色卡暂存目录初始化
    if not os.path.exists("data"):
        os.makedirs("data")
    if not os.path.exists(_cachepath):
        with open(_cachepath, "w", encoding="utf-8") as f:
            f.write("{}")
    cards.load()


def is_group_message() -> Rule:
    async def _is_group_message(bot: "Bot", event: "MessageEvent") -> bool:
        return True if type(event) is GroupMessageEvent else False

    return Rule(_is_group_message)


rdhelp = on_startswith(".help", priority=2, block=True)
stcommand = on_startswith(".st", priority=2, block=True)
encommand = on_startswith(".en", priority=2, block=True)
ticommand = on_startswith(".ti", priority=2, block=True)
licommand = on_startswith(".li", priority=2, block=True)
coccommand = on_startswith(".coc", priority=2, block=True)
sccommand = on_startswith(".sc", priority=2, block=True)
rdcommand = on_startswith(".r", priority=4, block=True)
setcommand = on_startswith(".set", priority=5, block=True)
showcommand = on_startswith(".show", priority=5, block=True)
sacommand = on_startswith(".sa", priority=5, block=True)
delcommand = on_startswith(".del", priority=5, block=True)


@rdhelp.handle()
async def rdhelphandler(matcher: Matcher, event: MessageEvent):
    args = str(event.get_message())[5:].strip()
    await matcher.finish(help_message(args))


@stcommand.handle()
async def stcommandhandler(matcher: Matcher):
    await matcher.finish(st())


@encommand.handle()
async def enhandler(matcher: Matcher, event: MessageEvent):
    args = str(event.get_message())[3:].strip()
    await matcher.finish(en(args))


@rdcommand.handle()
async def rdcommandhandler(event: MessageEvent):
    args = str(event.get_message())[2:].strip()
    uid = event.get_user_id()
    self_id = event.self_id
    bot = get_bot(str(self_id))
    assert isinstance(bot, Bot)
    if args and not ("." in args):
        rrd = rd(args)
        if type(rrd) == str:
            await rdcommand.finish(rrd)
        elif type(rrd) == list:
            await bot.send_private_msg(user_id=uid, message=rrd[0])


@coccommand.handle()
async def cochandler(matcher: Matcher, event: MessageEvent):
    args = str(event.get_message())[4:].strip()
    try:
        args = int(args)
    except ValueError:
        args = 20
    inv = Investigator()
    await matcher.send(inv.age_change(args))
    if 15 <= args < 90:
        cache_cards.update(event, inv.__dict__, save=False)
        await matcher.finish(inv.output())


@ticommand.handle()
async def ticommandhandler(matcher: Matcher, ):
    await matcher.finish(ti())


@licommand.handle()
async def licommandhandler(matcher: Matcher, ):
    await matcher.finish(li())


@sccommand.handle()
async def schandler(matcher: Matcher, event: MessageEvent):
    args = str(event.get_message())[3:].strip().lower()
    await matcher.finish(sc(args, event=event))


@setcommand.handle()
async def sethandler(matcher: Matcher, event: MessageEvent):
    args = str(event.get_message())[4:].strip().lower()
    await matcher.finish(set_handler(event, args))


@showcommand.handle()
async def showhandler(matcher: Matcher, event: MessageEvent):
    args = str(event.get_message())[5:].strip().lower()
    for msg in show_handler(event, args):
        await matcher.send(msg)


@sacommand.handle()
async def sahandler(matcher: Matcher, event: MessageEvent):
    args = str(event.get_message())[3:].strip().lower()
    await matcher.finish(sa_handler(event, args))


@delcommand.handle()
async def delhandler(matcher: Matcher, event: MessageEvent):
    args = str(event.get_message())[4:].strip().lower()
    for msg in del_handler(event, args):
        await matcher.send(msg)
