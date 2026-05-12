import asyncio
import logging
import time

from src import config
from src.monitors import docker_monitor, system_monitor
from src.notifiers.telegram_notifier import TelegramNotifier

logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL, logging.INFO),
    format="%(asctime)s  %(levelname)-8s  %(name)s  %(message)s",
)
logger = logging.getLogger(__name__)


def _format_health_report(
    sys_snap: system_monitor.SystemSnapshot,
    docker_snap: docker_monitor.DockerSnapshot,
) -> str:
    lines = ["*Project Goblin — Health Report*\n"]

    lines.append("*System*")
    lines.append(f"CPU: {sys_snap.cpu_percent:.1f}%")
    lines.append(
        f"RAM: {sys_snap.ram_percent:.1f}%  "
        f"({sys_snap.ram_used_gb}/{sys_snap.ram_total_gb} GB)"
    )
    lines.append(
        f"Disk: {sys_snap.disk_percent:.1f}%  "
        f"({sys_snap.disk_used_gb}/{sys_snap.disk_total_gb} GB)"
    )

    lines.append("\n*Containers*")
    if docker_snap.error:
        lines.append(f"⚠️ Docker error: {docker_snap.error}")
    elif not docker_snap.containers:
        lines.append("No containers found.")
    else:
        for c in docker_snap.containers:
            icon = "✅" if c.status == "running" else "❌"
            lines.append(f"{icon} `{c.name}` — {c.status}")
            if c.restart_count > 0:
                lines.append(f"   ↻ restarted {c.restart_count}×")

    return "\n".join(lines)


def _has_anomaly(
    sys_snap: system_monitor.SystemSnapshot,
    docker_snap: docker_monitor.DockerSnapshot,
) -> bool:
    if docker_snap.error:
        return True
    for c in docker_snap.containers:
        if c.status != "running":
            return True
        if c.restart_count > 0:
            return True
    if sys_snap.cpu_percent >= config.CPU_ALERT_THRESHOLD:
        return True
    if sys_snap.ram_percent >= config.RAM_ALERT_THRESHOLD:
        return True
    if sys_snap.disk_percent >= config.DISK_ALERT_THRESHOLD:
        return True
    return False


async def poll_once(notifier: TelegramNotifier) -> None:
    logger.info("Polling system and Docker health...")

    sys_snap = system_monitor.collect()
    docker_snap = docker_monitor.collect()

    if _has_anomaly(sys_snap, docker_snap):
        report = _format_health_report(sys_snap, docker_snap)
        logger.info("Anomaly detected — sending Telegram alert")
        await notifier.send(report)
    else:
        logger.info(
            "All healthy — CPU=%.1f%% RAM=%.1f%% Disk=%.1f%%",
            sys_snap.cpu_percent,
            sys_snap.ram_percent,
            sys_snap.disk_percent,
        )


async def run() -> None:
    notifier = TelegramNotifier()

    ok = await notifier.verify_connection()
    if not ok:
        logger.error("Cannot reach Telegram — check TELEGRAM_BOT_TOKEN. Exiting.")
        return

    logger.info(
        "Agent started. Poll interval: %ds", config.POLL_INTERVAL_SECONDS
    )
    await notifier.send("*Project Goblin started* ✅\nMonitoring your stack.")

    while True:
        try:
            await poll_once(notifier)
        except Exception as exc:  # noqa: BLE001
            logger.exception("Unhandled error in poll loop: %s", exc)
        await asyncio.sleep(config.POLL_INTERVAL_SECONDS)


def main() -> None:
    asyncio.run(run())


if __name__ == "__main__":
    main()
