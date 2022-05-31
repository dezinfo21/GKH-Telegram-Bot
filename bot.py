import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.fsm_storage.redis import RedisStorage2

from tgbot import middlewares, filters, handlers
from tgbot.data.config import load_config
from tgbot.utils import language
from tgbot.utils.misc import on_startup, on_shutdown

log = logging.getLogger(__name__)
config = load_config(".env")


async def main():
    from tgbot.utils import logging

    logging.setup()
    log.info("Starting bot...")

    language.setup()

    storage = RedisStorage2() if config.tg_bot.use_redis else MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')
    dp = Dispatcher(bot, storage=storage)

    bot['config'] = config

    middlewares.setup(dp)
    filters.setup(dp)
    handlers.setup(dp)

    try:
        await on_startup(dp)

        await dp.skip_updates()
        await dp.start_polling()

        await on_shutdown(dp)
    finally:
        log.info("Finishing bot...")

        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except(KeyboardInterrupt, SystemExit):
        log.error("Bot stopped!")
