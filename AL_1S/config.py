# python3
# -*- coding: utf-8 -*-
# @Time     : 2022/6/19
# @Author   : Vikala_Miki
# @Email    : Vikala.Miki@gmail.com
# @Github   : https://github.com/VikalaMiki
# @File     : config.py
# @Software : PyCharm
from datetime import timedelta
from ipaddress import IPv4Address
from pathlib import Path

import yaml


def load_yml(file: Path, encoding="utf-8") -> dict:
    with open(file, "r", encoding=encoding) as f:
        data = yaml.safe_load(f)
    return data


CONFIG_PATH = Path(".") / "config.yml"
config = load_yml(CONFIG_PATH)


class BotSelfConfig:
    config: dict = config["BotSelfConfig"]

    host: IPv4Address = IPv4Address(config.get("host", "127.0.0.1"))
    port: int = int(config.get("port", 8080))
    debug: bool = bool(config.get("debug", False))
    superusers: set = set(config.get("superusers", ["1303030112"]))
    nickname: set = set(config.get("nickname", ["AL-1S", "AL1S", "al-1s", "al1s",
                                                "ALICE", "Alice", "alice",
                                                "天童爱丽丝", "爱丽丝", "アリス", "天童アリス"]))
    command_start: set = set(config.get("command_start", [""]))
    command_sep: set = set(config.get("command_sep", ["."]))
    session_expire_timeout: timedelta = timedelta(
        seconds=config.get("session_expire_timeout", 60)
    )
    proxy: str = config.get("proxy", None)


class InlineGoCQHTTP:
    config: dict = config["InlineGoCQHTTP"]

    enabled: bool = bool(config.get("enabled", True))
    accounts: list = config.get("accounts", [])
    download_domain: str = config.get("download_domain", "download.fastgit.org")
    download_version: str = str(config.get("download_version", "v1.0.0-rc1"))


class YgoCard:
    config: dict = config["YgoCard"]


class AiDrawer:
    config: dict = config["AiDrawer"]

    wenxin_ak: str = str(config.get("wenxin_ak", ""))
    wenxin_sk: str = str(config.get("wenxin_sk", ""))
    wenxin_cd_time: int = int(config.get("wenxin_cd_time", 60))
    wenxin_image_count: int = int(config.get("wenxin_image_count", 1))
    wenxin_manager_list: list = list(config.get("wenxin_manager_list", ["1303030112"]))


class BotStatus:
    config: dict = config["BotStatus"]

    server_status_only_superusers: bool = bool(config.get("server_status_only_superusers", True))
    server_status_cpu: bool = bool(config.get("server_status_cpu", False))
    server_status_per_cpu: bool = bool(config.get("server_status_per_cpu", False))
    server_status_memory: bool = bool(config.get("server_status_memory", False))
    server_status_disk: bool = bool(config.get("server_status_disk", True))


class HikariImageSearch:
    config: dict = config["HikariImageSearch"]

    hikari_search_api: str = str(config.get("hikari_search_api", "https://hikari.obfs.dev"))
    hikari_search_max_results: int = int(config.get("hikari_search_max_results", 1))
    hikari_search_withdraw: int = int(config.get("hikari_search_withdraw", 30))


class TarotDivination:
    config: dict = config["TarotDivination"]

    chain_reply: bool = bool(config.get("chain_reply", True))
    nickname: set = set(config.get("nickname", ["AL-1S", "AL1S", "al-1s", "al1s",
                                                "ALICE", "Alice", "alice",
                                                "天童爱丽丝", "爱丽丝", "アリス", "天童アリス"]))


RUNTIME_CONFIG = {
    "host": BotSelfConfig.host,
    "port": BotSelfConfig.port,
    "debug": BotSelfConfig.debug,
    "superusers": BotSelfConfig.superusers,
    "nickname": BotSelfConfig.nickname,
    "command_start": BotSelfConfig.command_start,
    "command_sep": BotSelfConfig.command_sep,
    "session_expire_timeout": BotSelfConfig.session_expire_timeout,
    "gocq_accounts": InlineGoCQHTTP.accounts,
    "gocq_download_domain": InlineGoCQHTTP.download_domain,
    "gocq_version": InlineGoCQHTTP.download_version,
}
