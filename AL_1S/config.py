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
    ex_cookie: str = config.get("ex_cookie", None)
    search_limit: int = int(config.get("search_limit", 2))
    risk_control: bool = bool(config.get("risk_control", True))
    record_priority: int = int(config.get("record_priority", 99))


class InlineGoCQHTTP:
    config: dict = config["InlineGoCQHTTP"]

    enabled: bool = bool(config.get("enabled", True))
    accounts: list = config.get("accounts", [])
    download_domain: str = config.get("download_domain", "download.fastgit.org")
    download_version: str = str(config.get("download_version", "v1.0.0-rc1"))


# class SauceNAO:
#     config: dict = config["SauceNAO"]
#
#     key: str = config.get("key", "")
#
#
# class Setu:
#     config: dict = config["Setu"]
#
#     reverse_proxy: bool = bool(config.get("reverse_proxy", False))
#     reverse_proxy_domain: str = config.get("reverse_proxy_domain", str())


# class BotStatus:
#     config: dict = config["BotStatus"]
#
#     server_status_only_superusers: bool = bool(config.get("server_status_only_superusers", True))
#     superusers: set = set(config.get("superusers", ["1303030112"]))
# server_status_template: str = config.get("server_status_template", "")


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
