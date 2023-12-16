from aiogram import Bot, Dispatcher, F
import asyncio
from core.handlers.basic import get_start, find_shoes
from core.settings import settings
import logging
from core.utils.commands import set_commands


async def start_bot(bot: Bot):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, 'Bot has started')


async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, 'Bot has stopped')


async def start():
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s - [%(levelname)s] - %(name)s"
                               "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
                        )
    bot = Bot(token=settings.bots.bot_token)
    dp = Dispatcher()

    dp.message.register(get_start, F.text == '/start')
    dp.message.register(find_shoes, F.text == 'Знайти шузи')
    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


if __name__ == '__main__':
    asyncio.run(start())
