import asyncio
import logging

from telegram import Bot
from telegram.error import TelegramError

from src import config

logger = logging.getLogger(__name__)


class TelegramNotifier:
    def __init__(self) -> None:
        self._bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
        self._chat_id = config.TELEGRAM_CHAT_ID

    async def send(self, text: str) -> bool:
        try:
            await self._bot.send_message(
                chat_id=self._chat_id,
                text=text,
                parse_mode="Markdown",
            )
            logger.debug("Telegram message sent (%d chars)", len(text))
            return True
        except TelegramError as exc:
            logger.error("Telegram send failed: %s", exc)
            return False

    def send_sync(self, text: str) -> bool:
        return asyncio.run(self.send(text))

    async def verify_connection(self) -> bool:
        try:
            me = await self._bot.get_me()
            logger.info("Telegram bot connected: @%s", me.username)
            return True
        except TelegramError as exc:
            logger.error("Telegram connection failed: %s", exc)
            return False
