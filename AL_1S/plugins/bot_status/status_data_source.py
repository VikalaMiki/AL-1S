#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from datetime import timedelta
from typing import Dict, List

import psutil


def cpu_status() -> float:
    return psutil.cpu_percent(interval=1)  # type: ignore


def per_cpu_status() -> List[float]:
    return psutil.cpu_percent(interval=1, percpu=True)  # type: ignore


def memory_status() -> float:
    return psutil.virtual_memory().percent


def disk_usage() -> Dict[str, psutil._common.sdiskusage]:
    disk_parts = psutil.disk_partitions()
    return {d.mountpoint: psutil.disk_usage(d.mountpoint) for d in disk_parts}


def uptime() -> timedelta:
    diff = time.time() - psutil.boot_time()
    return timedelta(seconds=diff)


if __name__ == "__main__":
    print(cpu_status())
    print(memory_status())
    print(disk_usage())
