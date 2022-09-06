from pathlib import Path
from typing import Set

import nonebot
from pydantic import BaseModel, Extra

from AL_1S.config import TarotDivination

try:
    import ujson as json
except ModuleNotFoundError:
    import json


class TarotConfig(BaseModel, extra=Extra.ignore):
    tarot_path: Path = Path(__file__).parent / "resource"
    chain_reply: bool = TarotDivination.chain_reply
    nickname: Set[str] = TarotDivination.nickname


driver = nonebot.get_driver()
tarot_config: TarotConfig = TarotConfig.parse_obj(driver.config.dict())
