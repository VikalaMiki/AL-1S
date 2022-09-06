#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import warnings
from typing import Any, Dict

import nonebot
from pydantic import BaseSettings, root_validator

from AL_1S.config import BotStatus

CPU_TEMPLATE = "CPU: {{ '%02d' % cpu_usage }}%"
PER_CPU_TEMPLATE = (
    "CPU:\n"
    "{%- for core in per_cpu_usage %}\n"
    "  core{{ loop.index }}: {{ '%02d' % core }}%\n"
    "{%- endfor %}"
)
MEMORY_TEMPLATE = "Memory: {{ '%02d' % memory_usage }}%"
DISK_TEMPLATE = (
    "Disk:\n"
    "{%- for name, usage in disk_usage.items() %}\n"
    "  {{ name }}: {{ '%02d' % usage.percent }}%\n"
    "{%- endfor %}"
)
UPTIME_TEMPLATE = "Uptime: {{ uptime }}"


class Config(BaseSettings):
    server_status_only_superusers: bool = BotStatus.server_status_only_superusers

    # Deprecated: legacy settings
    server_status_cpu: bool = BotStatus.server_status_cpu
    server_status_per_cpu: bool = BotStatus.server_status_per_cpu
    server_status_memory: bool = BotStatus.server_status_memory
    server_status_disk: bool = BotStatus.server_status_disk

    # template
    server_status_template: str = "\n".join(
        (CPU_TEMPLATE, MEMORY_TEMPLATE, DISK_TEMPLATE, UPTIME_TEMPLATE)
    )

    class Config:
        extra = "ignore"

    @root_validator(pre=True)
    def transform_legacy_settings(self, value: Dict[str, Any]) -> Dict[str, Any]:
        if "server_status_template" not in value and (
                "server_status_cpu" in value
                or "server_status_per_cpu" in value
                or "server_status_memory" in value
                or "server_status_disk" in value
        ):
            warnings.warn(
                "Settings for status plugin is deprecated, "
                "please use `server_status_template` instead.",
                DeprecationWarning,
            )
            templates = []
            if value.get("server_status_cpu"):
                templates.append(CPU_TEMPLATE)
            if value.get("server_status_per_cpu"):
                templates.append(PER_CPU_TEMPLATE)
            if value.get("server_status_memory"):
                templates.append(MEMORY_TEMPLATE)
            if value.get("server_status_disk"):
                templates.append(DISK_TEMPLATE)
            value.setdefault("server_status_template", "\n".join(templates))

        return value


config = Config.parse_obj(nonebot.get_driver().config.dict())  # 载入配置
