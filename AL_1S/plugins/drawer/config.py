from typing import List

import nonebot
from pydantic import BaseSettings

from AL_1S.config import AiDrawer

driver = nonebot.get_driver()


class Config(BaseSettings):
    wenxin_ak: str = AiDrawer.wenxin_ak  # 文心大模型的ak
    wenxin_sk: str = AiDrawer.wenxin_sk  # 文心大模型的sk
    wenxin_cd_time: int = AiDrawer.wenxin_cd_time  # cd时间，单位秒
    wenxin_image_count: int = AiDrawer.wenxin_image_count  # 画画的图片数量
    wenxin_manager_list: List[str] = AiDrawer.wenxin_manager_list  # 文心大模型的管理员列表（不受冷却时间限制）

    class Config:
        extra = "ignore"


config = Config.parse_obj(driver.config.dict())  # 载入配置
