import os
from dotenv import load_dotenv

load_dotenv()


def _require(key: str) -> str:
    value = os.getenv(key)
    if not value:
        raise EnvironmentError(f"Required environment variable not set: {key}")
    return value


def _int(key: str, default: int) -> int:
    return int(os.getenv(key, default))


ANTHROPIC_API_KEY = _require("ANTHROPIC_API_KEY")
TELEGRAM_BOT_TOKEN = _require("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = _require("TELEGRAM_CHAT_ID")

JELLYFIN_CONTAINER_NAME = os.getenv("JELLYFIN_CONTAINER_NAME", "jellyfin")
DOCKER_SOCKET_PATH = os.getenv("DOCKER_SOCKET_PATH", "/var/run/docker.sock")

POLL_INTERVAL_SECONDS = _int("POLL_INTERVAL_SECONDS", 60)
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()

CPU_ALERT_THRESHOLD = _int("CPU_ALERT_THRESHOLD", 90)
RAM_ALERT_THRESHOLD = _int("RAM_ALERT_THRESHOLD", 85)
DISK_ALERT_THRESHOLD = _int("DISK_ALERT_THRESHOLD", 90)
