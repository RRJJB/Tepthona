from Tepthon.core.client import TepthonClient
from Tepthon.config import Var

# تشغيل الحساب الأساسي
jmubot = jmthon_bot = TepthonClient(
    session=StringSession(Var.SESSION),
    api_id=Var.API_ID,
    api_hash=Var.API_HASH
)
jmubot.run_in_loop(jmubot.start_client())

# تشغيل البوت المساعد (Tgbot)
tgbot = asst = TepthonClient("Tgbot")
tgbot.run_in_loop(tgbot.start_client(bot_token=Var.BOT_TOKEN))