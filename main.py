from aiogram import Bot, Dispatcher, F, types
from aiogram.enums import ParseMode
from core.handlers.basic import router, get_start, find_shoes
import logging
from aiohttp import web

from core.settings import settings
from core.utils.commands import set_commands

BASE_WEBHOOK_URL = 'https://fcbd-193-34-172-202.ngrok-free.app'
API_TOKEN = settings.bots.bot_token


async def on_startup(_):
    await set_commands(bot)
    await bot.send_message(settings.bots.admin_id, 'Bot has started')
    await bot.set_webhook(
        f"{BASE_WEBHOOK_URL}/{API_TOKEN}"
    )


async def on_shutdown(_):
    await bot.send_message(settings.bots.admin_id, 'Bot has stopped')


async def catch_webhook(request: web.Request):
    token = str(request.url).split('/')[-1]
    if token == API_TOKEN:
        request_data = await request.json()
        update = types.Update(**request_data)
        await dp._process_update(update=update, bot=bot)
        return web.Response()
    else:
        return web.Response(status=403)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format=("%(asctime)s - [%(levelname)s] - %(name)s"
                "(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s")
    )
    bot = Bot(token=settings.bots.bot_token, parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(router=router)

    # dp.message.register(get_start, F.text == '/start')
    dp.message.register(find_shoes, F.text == 'Знайти шузи')

    app = web.Application()
    app.router.add_post(f'/{API_TOKEN}', catch_webhook)
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    web.run_app(
        app,
        host='0.0.0.0',
        port=8888
    )
