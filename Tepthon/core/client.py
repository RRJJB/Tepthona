import contextlib
import inspect
import os
import sys
import time
from datetime import datetime
from logging import Logger

from telethon import hints, utils, TelegramClient
from telethon.errors import (
    AccessTokenExpiredError,
    AccessTokenInvalidError,
    ApiIdInvalidError,
    AuthKeyDuplicatedError,
)
from telethon.sessions import StringSession
from telethon.tl.types import User

from Tepthon.config import Var
from database import jmdB
from Tepthon.core.helper import fast_download
from Tepthon.core.logger import LOGS, TelethonLogger
from resources import blacklisted_users


class TepthonClient(TelegramClient):
    me: User

    def __init__(
        self,
        session,
        api_id: int = Var.API_ID,
        api_hash: str = Var.API_HASH,
        logger: Logger = LOGS,
        log_attempt=True,
        exit_on_error=True,
        *args,
        **kwargs,
    ):
        self._cache = {}
        self._dialogs = []
        self._handle_error = exit_on_error
        self._log_at = log_attempt
        self.logger = logger
        self._thumb = {}
        kwargs["base_logger"] = TelethonLogger

        super().__init__(
            session,
            api_id=api_id,
            api_hash=api_hash,
            connection_retries=10,
            retry_delay=2,
            auto_reconnect=True,
            *args,
            **kwargs,
        )
        self.parse_mode = "html"

    async def start_client(self, bot_token=None):
        if self._log_at:
            self.logger.info("❃ جاري تسجيل الدخول...")
        try:
            await self.start(bot_token=bot_token)
        except ApiIdInvalidError:
            self.logger.critical("◙ الأيبي أيدي والأيبي هاش غير متطابقين")
            sys.exit()
        except (AuthKeyDuplicatedError, EOFError):
            if self._handle_error:
                self.logger.critical("⎆ كود السيشن أو التوكن منتهي اصنع كود جديد وأضفه إلى المتغيرات...")
                return sys.exit()
            self.logger.critical("❃ سيشن الحساب/توكن الحساب منتهي الصلاحية.")
        except (AccessTokenExpiredError, AccessTokenInvalidError):
            jmdB.del_key("BOT_TOKEN")
            self.logger.critical(
                "❃ توكن البوت منتهي أو غير صالح، اصنع بوت جديد من @Botfather وأضفه مع المتغير BOT_TOKEN"
            )
            sys.exit()
        self.me = await self.get_me()
        if self.me.bot:
            me = f"@{self.me.username}"
        else:
            setattr(self.me, "phone", None)
            me = self.full_name
        if self.uid in blacklisted_users:
            self.logger.error(
                f"({me} - {self.uid}) ~ لا يمكنك استخدام سورس تيبثون أنت محظور بسبب مخالفتك سياسة الاستخدام @Tepthon"
            )
            sys.exit(1)
        if self._log_at:
            self.logger.info(f"❃ تم تسجيل الدخول كـ {me}")
        self._bot = await self.is_bot()

    def run_in_loop(self, function):
        return self.loop.run_until_complete(function)

    def run(self):
        self.run_until_disconnected()

    def add_handler(self, func, *args, **kwargs):
        if func in list(map(lambda e: e[0], self.list_event_handlers())):
            return
        self.add_event_handler(func, *args, **kwargs)

    @property
    def full_name(self):
        return utils.get_display_name(self.me)

    @property
    def uid(self):
        return self.me.id

    def to_dict(self):
        return dict(inspect.getmembers(self))