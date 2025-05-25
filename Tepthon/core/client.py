from . import *
import sys
import time
from Tepthon.core.helper import time_formatter
from Tepthon.load_plug import load
from telethon.errors import SessionRevokedError
from .utils import join_dev, main_process
from Tepthon.config import Var
from telethon.sessions import StringSession
from Tepthon.core.client import TepthonClient

start_time = time.time()

# إنشاء الكلاينت
jmubot = TepthonClient(
    session=StringSession(Var.SESSION),
    api_id=Var.API_ID,
    api_hash=Var.API_HASH
)

# تسجيل الدخول
jmubot.run_in_loop(jmubot.start_client(bot_token=Var.BOT_TOKEN))

# الآن يمكن التعامل مع .me
if not jmubot.me.bot:
    setattr(jmubot.me, "phone", None)
    jmdB.set_key("OWNER_ID", jmubot.me.id)
    jmdB.set_key("NAME", jmubot.full_name)

LOGS.info("جاري تثبيت تيبثون...")

try:
    LOGS.info("- يتم إعـداد الإعدادات .......")
    jmubot.loop.run_until_complete(main_process())
    LOGS.info("تم إعداد إعدادات تيبثون ✅")
except Exception as meo:
    LOGS.error(f"- {meo}")
    sys.exit()

jmubot.loop.create_task(join_dev())

async def load_plugins():
    load(["plugins/basic", "plugins/assistant", "plugins/account", "plugins/fun", "plugins/group"])

jmubot.run_in_loop(load_plugins())

LOGS.info(f"⏳ تم استغراق {time_formatter((time.time() - start_time) * 1000)} ميللي ثانية لبدء تشغيل سورس تيبثون.")

LOGS.info(
    """
    ╔══════════════════════════════════════════╗
    ║       ✅ تم تنصيب وتشغيل سورس تيبثون بنجاح             ║ 
    ║       تابع آخر التحديثات من خلال قناة @Tepthon            ║
    ╚══════════════════════════════════════════╝
    """
)

try:
    asst.run()
    LOGS.info(f"تم بنجاح تشغيل البوت المساعد من @Tepthon")
except SessionRevokedError:
    LOGS.info(f"جلسة البوت المساعد [@{asst.me.username}] فشلت لكن سيتم تشغيل سورس الحساب فقط")
    jmubot.run()
