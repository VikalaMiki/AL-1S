from pathlib import Path
from typing import Set

import nonebot
from pydantic import BaseModel, Extra

try:
    import ujson as json
except ModuleNotFoundError:
    import json


class TarotConfig(BaseModel, extra=Extra.ignore):
    tarot_path: Path = Path(__file__).parent / "resource"
    chain_reply: bool = True
    nickname: Set[str] = {"Bot"}


driver = nonebot.get_driver()
tarot_config: TarotConfig = TarotConfig.parse_obj(driver.config.dict())
