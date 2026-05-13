import logging
from dataclasses import dataclass

import psutil

logger = logging.getLogger(__name__)


@dataclass
class SystemSnapshot:
    cpu_percent: float
    ram_percent: float
    ram_used_gb: float
    ram_total_gb: float
    disk_percent: float
    disk_used_gb: float
    disk_total_gb: float


def collect() -> SystemSnapshot:
    cpu = psutil.cpu_percent(interval=1)

    ram = psutil.virtual_memory()
    disk = psutil.disk_usage("/")

    snapshot = SystemSnapshot(
        cpu_percent=cpu,
        ram_percent=ram.percent,
        ram_used_gb=round(ram.used / 1024**3, 2),
        ram_total_gb=round(ram.total / 1024**3, 2),
        disk_percent=disk.percent,
        disk_used_gb=round(disk.used / 1024**3, 2),
        disk_total_gb=round(disk.total / 1024**3, 2),
    )
    logger.debug(
        "System snapshot: CPU=%.1f%% RAM=%.1f%% Disk=%.1f%%",
        snapshot.cpu_percent,
        snapshot.ram_percent,
        snapshot.disk_percent,
    )
    return snapshot
