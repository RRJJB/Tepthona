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
from telethon.tl.types import User

from Tepthon.config import Var
from database import jmdB
from Tepthon.core.helper import fast_download
from Tepthon.core.logger import LOGS, TelethonLogger
from resources import blacklisted_users

class TepthonClient(TelegramClient):
    me: User

    def __init__(self, session, api_id: int = Var.API_ID, api_hash: str = Var.API_HASH,
                 bot_token=None, logger: Logger = LOGS, log_attempt=True, exit_on_error=True, *args, **kwargs):
        self._cache = {}
        self._dialogs = []
        self._handle_error = exit_on_error
        self._log_at = log_attempt
        self.logger = logger
        self._thumb = {}
        kwargs["base_logger"] = TelethonLogger
        super().__init__(session, api_id=api_id, api_hash=api_hash, **kwargs)
        self.run_in_loop(self.start_client(bot_token=bot_token))
        self.dc_id = self.session.dc_id

    def __repr__(self):
        return f"<Tepthon Client :\n self: {self.full_name}\n bot: {self._bot}\n>"

    @property
    def __dict__(self):
        if self.me:
            return self.me.to_dict()

    async def start_client(self, **kwargs):
        if self._log_at:
            self.logger.info("❃ جاري تسجيل الدخول...")
        try:
            await self.start(**kwargs)
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
            self.logger.critical("❃ توكن البوت منتهي أو غير صالح، اصنع بوت جديد من @Botfather وأضفه مع المتغير BOT_TOKEN")
            sys.exit()
        self.me = await self.get_me()
        if self.me.bot:
            me = f"@{self.me.username}"
        else:
            setattr(self.me, "phone", None)
            me = self.full_name
        if self.uid in blacklisted_users:
            self.log.error(f"({me} - {self.uid}) ~ لا يمكنك استخدام سورس تيبثون أنت محظور بسبب مخالفتك سياسة الاستخدام @Tepthon")
            sys.exit(1)
        if self._log_at:
            self.logger.info(f"❃ تم تسجيل الدخول كـ {me}")
        self._bot = await self.is_bot()

    
