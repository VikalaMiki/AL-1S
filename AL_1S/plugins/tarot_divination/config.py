from pathlib import Path
from typing import Set

import nonebot
from pydantic import BaseModel, Extra

try:
    import ujson as json
except ModuleNotFoundError:
    import json


class PluginConfig(BaseModel, extra=Extra.ignore):
    tarot_path: Path = Path(__file__).parent / "resource"
    chain_reply: bool = False
    nickname: Set[str] = {"Bot"}


driver = nonebot.get_driver()
tarot_config: PluginConfig = PluginConfig.parse_obj(driver.config.dict())
